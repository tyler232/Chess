#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <time.h>

#define SERVER_IP "127.0.0.1"  // Changed to explicit loopback address
#define SERVER_PORT 9060
#define MAX_CLIENTS 2
#define BUFFER_SIZE 4096

int clients[MAX_CLIENTS];
int client_count = 0;
pthread_mutex_t client_lock;

void *handle_client(void *arg) {
    int conn = *(int *)arg;
    free(arg);  // Free the dynamically allocated memory after extracting conn
    struct sockaddr_in addr;
    socklen_t addr_len = sizeof(addr);
    getpeername(conn, (struct sockaddr *)&addr, &addr_len);
    printf("Connected to %s:%d\n", inet_ntoa(addr.sin_addr), ntohs(addr.sin_port));

    while (1) {
        char buffer[BUFFER_SIZE];
        ssize_t bytes_received = recv(conn, buffer, sizeof(buffer), 0);
        if (bytes_received <= 0) {
            break;
        }

        printf("Move received from %s:%d\n", inet_ntoa(addr.sin_addr), ntohs(addr.sin_port));

        pthread_mutex_lock(&client_lock);
        for (int i = 0; i < client_count; i++) {
            if (clients[i] != conn) {
                send(clients[i], buffer, bytes_received, 0);
            }
        }
        pthread_mutex_unlock(&client_lock);
    }

    printf("Disconnected from %s:%d\n", inet_ntoa(addr.sin_addr), ntohs(addr.sin_port));
    pthread_mutex_lock(&client_lock);
    for (int i = 0; i < client_count; i++) {
        if (clients[i] == conn) {
            clients[i] = clients[--client_count];
            break;
        }
    }
    pthread_mutex_unlock(&client_lock);
    close(conn);
    return NULL;
}

int main() {
    pthread_mutex_init(&client_lock, NULL);

    // Create the server socket
    int server = socket(AF_INET, SOCK_STREAM, 0);
    if (server < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Setup the server address structure
    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr(SERVER_IP);  // Explicit loopback address
    server_addr.sin_port = htons(SERVER_PORT);

    // Bind the socket to the server address and port
    if (bind(server, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Bind failed");
        close(server);
        exit(EXIT_FAILURE);
    }

    // Listen for incoming connections
    if (listen(server, MAX_CLIENTS) < 0) {
        perror("Listen failed");
        close(server);
        exit(EXIT_FAILURE);
    }

    printf("Server started. Waiting for clients to connect on %s:%d...\n", SERVER_IP, SERVER_PORT);

    // Accept clients
    while (client_count < MAX_CLIENTS) {
        int *conn = malloc(sizeof(int));  // Allocate memory for each connection
        if ((*conn = accept(server, NULL, NULL)) < 0) {
            perror("Accept failed");
            free(conn);  // Free the allocated memory if accept fails
            continue;
        }

        // Add client to the list
        pthread_mutex_lock(&client_lock);
        clients[client_count++] = *conn;
        pthread_mutex_unlock(&client_lock);

        pthread_t thread;
        pthread_create(&thread, NULL, handle_client, conn);  // Pass the connection pointer
        pthread_detach(thread);
    }

    printf("Both clients connected. Starting the game...\n");

    // Assign colors to clients
    srand(time(NULL));
    for (int i = 0; i < client_count; i++) {
        const char *color = (i == 0) ? "WHITE" : "BLACK";
        send(clients[i], color, strlen(color) + 1, 0);
    }

    // Keep the server running
    while (1) {
        pause();
    }

    // Clean up when shutting down
    for (int i = 0; i < client_count; i++) {
        close(clients[i]);
    }
    close(server);
    pthread_mutex_destroy(&client_lock);

    return 0;
}
