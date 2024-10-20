#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <time.h>
#include <errno.h>
#include <signal.h>

#define DEFAULT_SERVER_IP "127.0.0.1"
#define DEFAULT_SERVER_PORT 9060
#define MAX_CLIENTS 2
#define BUFFER_SIZE 4096
#define RECONNECT_TIMEOUT 60
#define WAITING_OPPONENT_SIGNAL "WAIT\n"
#define NO_WAITING_OPPONENT_SIGNAL "NOWA\n"
#define START_GAME_SIGNAL "STRT\n"
#define RECONNECT_SIGNAL "RECN\n"
#define RESTART_SIGNAL "RSTR\n"
#define ROOM_FULL_SIGNAL "FULL\n"
#define MAX_CONNECTION_ATTEMPTS 512

char* server_ip = DEFAULT_SERVER_IP;
int server_port = DEFAULT_SERVER_PORT;

typedef struct {
    int conn;
    char ip[INET_ADDRSTRLEN];
    int port;
    char *id;
    char color[8];
    time_t last_active;
} Client;

typedef struct {
    ssize_t size;
    char *data;
} BackupStorage;

int server_running = 1;
int server_socket;
Client clients[MAX_CLIENTS];
BackupStorage *progress = NULL;
int client_count = 0;
int connection_attempts = 0;    // stress protection
pthread_mutex_t client_lock;

void cleanup();

void signal_handler(int signum) {
    server_running = 0;
    cleanup();
    exit(0);
}

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

// Read from client until newline character
ssize_t read_until_nl(int socket, char *buffer, size_t count) {
    size_t total_bytes_read = 0;
	size_t bytes_read;

    if (count <= 0 || buffer == NULL) {
        errno = EINVAL;
        return -1;
    }

    while (1) {
		char curr_char;
        bytes_read = read(socket, &curr_char, 1);

        if (bytes_read < 0) {
            if (errno == EINTR) {
				continue;
			} else {
				return -1;
			}
        } else if (bytes_read == 0) {
            if (total_bytes_read == 0) return 0;
			return total_bytes_read;
		}

        if (total_bytes_read < count - 1) {
            total_bytes_read++;
            *buffer++ = curr_char;
        }

        if (curr_char == '\n') break;
    }

    return total_bytes_read;
}

int find_client_by_id(const char *id) {
    for (int i = 0; i < client_count; i++) {
        if (strcmp(clients[i].id, id) == 0) {
            return i;
        }
    }
    return -1;
}

void cleanup() {
    for (int i = 0; i < client_count; i++) {
        close(clients[i].conn);
        free(clients[i].id);
    }

    if (progress != NULL) {
        if (progress->data != NULL) free(progress->data);
        free(progress);
    }
    pthread_mutex_destroy(&client_lock);
    close(server_socket);
    printf("Server cleaned up and shutting down.\n");
}

void *handle_client(void *arg) {
    int conn = *(int *)arg;
    free(arg);  // Free the dynamically allocated memory after extracting conn
    struct sockaddr_in addr;
    socklen_t addr_len = sizeof(addr);
    getpeername(conn, (struct sockaddr *)&addr, &addr_len);
    char *client_ip = inet_ntoa(addr.sin_addr);
    int client_port = ntohs(addr.sin_port);

    char id[BUFFER_SIZE];
    read_until_nl(conn, id, sizeof(id));    // read the client id
    id[strlen(id) - 1] = '\0';  // remove the newline character
    printf("Connected to %s:%d, id: %s\n", client_ip, client_port, id);

    // Check if the client is connected before
    pthread_mutex_lock(&client_lock);
    int client_index = find_client_by_id(id);
    if (client_index == -1) {  // New connection
        client_index = client_count++;
        strcpy(clients[client_index].ip, client_ip);
        clients[client_index].port = client_port;
        clients[client_index].conn = conn;
        clients[client_index].id = strdup(id);

        // Notify the client if there is another client waiting
        if (client_count == 1) send(conn, WAITING_OPPONENT_SIGNAL, 5, 0);
        else if (client_count == 2) {
            // or start the game if there are two clients connected
            send(clients[1].conn, NO_WAITING_OPPONENT_SIGNAL, 5, 0);
            send(clients[0].conn, START_GAME_SIGNAL, 5, 0);
            send(clients[1].conn, START_GAME_SIGNAL, 5, 0);

            const char *color[2];
            if (rand() % 2 == 0) {
                color[0] = "WHITE\n";
                color[1] = "BLACK\n";
            } else {
                color[0] = "BLACK\n";
                color[1] = "WHITE\n";
            }
            // Send the assigned color to the client
            printf("Assigning and sending color to clients\n");
            printf("Clients %s: %s\n", clients[0].id, color[0]);
            printf("Clients %s: %s\n", clients[1].id, color[1]);
            send(clients[0].conn, color[0], strlen(color[0]), 0);
            send(clients[1].conn, color[1], strlen(color[1]), 0);

            // Store the color for future reconnections
            strcpy(clients[0].color, color[0]);
            strcpy(clients[1].color, color[1]);

            // send oppoenent's id
            char client0_id_signal[BUFFER_SIZE];
            char client1_id_signal[BUFFER_SIZE];
            snprintf(client0_id_signal, sizeof(client0_id_signal), "%s\n", clients[0].id);
            snprintf(client1_id_signal, sizeof(client1_id_signal), "%s\n", clients[1].id);
            send(clients[0].conn, client1_id_signal, strlen(client1_id_signal), 0);
            send(clients[1].conn, client0_id_signal, strlen(client0_id_signal), 0);
        } else if (client_count > 2) {
            printf("Client %s: rejected. Game is full.\n", id);
            send(conn, ROOM_FULL_SIGNAL, 5, 0);
            close(conn);
            free(clients[client_index].id);
            client_count = 2;
        }
    } else { // Reconnection
        clients[client_index].conn = conn;
        strcpy(clients[client_index].ip, client_ip);
        clients[client_index].port = client_port;
        clients[client_index].conn = conn;
        printf("Client %s: reconnected.\n", id);
        // Notify the client that it is reconnected
        send(conn, RECONNECT_SIGNAL, 5, 0);
        send(conn, RESTART_SIGNAL, 5, 0);

        // Resend the color on reconnection
        const char *color = clients[client_index].color;
        send(conn, color, strlen(color), 0);

        // Resend the opponent's id
        char opponent_id_signal[BUFFER_SIZE];
        snprintf(opponent_id_signal, sizeof(opponent_id_signal), "%s\n", clients[1 - client_index].id);
        send(conn, opponent_id_signal, strlen(opponent_id_signal), 0);

        // Resend the progress to restore the game
        if (progress != NULL) {
            send(conn, progress->data, progress->size, 0);
        }
    }

    clients[client_index].last_active = time(NULL);
    pthread_mutex_unlock(&client_lock);

    while (1) {
        char buffer[BUFFER_SIZE];
        ssize_t bytes_received = recv(conn, buffer, sizeof(buffer), 0);
        if (bytes_received <= 0) {
            printf("Client %s disconnected.\n", id);
            break;
        }

        // Store the progress for backup
        if (progress->data != NULL) {
            free(progress->data);
        }
        progress->size = bytes_received;
        progress->data = (char *)malloc(progress->size);
        memcpy(progress->data, buffer, progress->size);

        // reset last active time of client
        pthread_mutex_lock(&client_lock);
        clients[client_index].last_active = time(NULL);
        pthread_mutex_unlock(&client_lock);
        
        printf("Move received from %s\n", id);
        printf("Forwarding the move to the other client...\n");

        pthread_mutex_lock(&client_lock);
        for (int i = 0; i < client_count; i++) {
            if (clients[i].conn != conn) {
                send(clients[i].conn, progress->data, progress->size, 0);
            }
        }
        pthread_mutex_unlock(&client_lock);
    }

    // Client disconnected, reserve the spot and allow reconnection
    printf("Disconnected from %s\n", id);
    pthread_mutex_lock(&client_lock);
    clients[client_index].conn = -1;
    pthread_mutex_unlock(&client_lock);
    close(conn);
    return NULL;
}

int main(int argc, char *argv[]) {
    parse_args(argc, argv);

    srand(time(NULL));
    progress = (BackupStorage *)malloc(sizeof(BackupStorage));
    pthread_mutex_init(&client_lock, NULL);
    signal(SIGINT, signal_handler);

    // Create the server socket
    int server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Setup the server address structure
    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr(server_ip);  // Explicit loopback address
    server_addr.sin_port = htons(server_port);

    // Bind the socket to the server address and port
    if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Bind failed");
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    // listen for incoming connections
    if (listen(server_socket, MAX_CLIENTS) < 0) {
        perror("Listen failed");
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    printf("Server started. Waiting for clients to connect on %s:%d...\n", server_ip, server_port);

    // Accept clients
    while (server_running) {
        connection_attempts++;
        int *conn = (int *)malloc(sizeof(int));
        if ((*conn = accept(server_socket, NULL, NULL)) < 0) {
            perror("Accept failed");
            free(conn);
            continue;
        }

        pthread_t thread;
        if (connection_attempts < MAX_CONNECTION_ATTEMPTS) {
            pthread_create(&thread, NULL, handle_client, conn);  // Pass the connection pointer
            pthread_detach(thread);
        }
        connection_attempts--;
    }

    printf("Both clients connected. Starting the game...\n");

    // Keep the server running
    while (server_running) {
        sleep(1);
        time_t current_time = time(NULL);

        // check if disconnected clients is timed out
        pthread_mutex_lock(&client_lock);
        for (int i = 0; i < client_count; i++) {
            if (clients[i].conn == -1 && difftime(current_time, clients[i].last_active) > RECONNECT_TIMEOUT) {
                printf("Client %s did not reconnect in time. Removing from the game.\n", clients[i].id);
                free(clients[i].id);
                clients[i] = clients[--client_count];
            }
        }

        pthread_mutex_unlock(&client_lock);
    }

    // Clean up when shutting down
    cleanup();
    return 0;
}

