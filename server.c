#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <time.h>

#define DEFAULT_SERVER_IP "127.0.0.1"
#define DEFAULT_SERVER_PORT 9060
#define MAX_CLIENTS 2
#define BUFFER_SIZE 4096

char* server_ip = DEFAULT_SERVER_IP;
int server_port = DEFAULT_SERVER_PORT;

int clients[MAX_CLIENTS];
int client_count = 0;
pthread_mutex_t client_lock;

void parse_args(int argc, char *argv[]) {
    if (argc > 1) {
        char *arg = strtok(argv[1], ":");
        if (arg != NULL) {
            server_ip = arg;
            arg = strtok(NULL, ":");
            if (arg != NULL) {
                server_port = atoi(arg);
            } else {
                printf("Usage: %s [ip:port]\n", argv[0]);
                exit(EXIT_FAILURE);
            }
        } else {
            printf("Usage: %s [ip:port]\n", argv[0]);
            exit(EXIT_FAILURE);
        }
    }
}

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

int main(int argc, char *argv[]) {
    parse_args(argc, argv);

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
    server_addr.sin_addr.s_addr = inet_addr(server_ip);  // Explicit loopback address
    server_addr.sin_port = htons(server_port);

    // Bind the socket to the server address and port
    if (bind(server, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Bind failed");
        close(server);
        exit(EXIT_FAILURE);
    }

    // listen for incoming connections
    if (listen(server, MAX_CLIENTS) < 0) {
        perror("Listen failed");
        close(server);
        exit(EXIT_FAILURE);
    }

    printf("Server started. Waiting for clients to connect on %s:%d...\n", server_ip, server_port);

    // Accept clients
    while (client_count < MAX_CLIENTS) {
        int *conn = (int *)malloc(sizeof(int));
        if ((*conn = accept(server, NULL, NULL)) < 0) {
            perror("Accept failed");
            free(conn);
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
    printf("Colors assigned to clients\n");

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

