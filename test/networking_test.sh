#!/bin/bash

# Compile the C server program
gcc -o server server.c

# Function to clean up processes
cleanup() {
    echo "Shutting down clients..."
    
    # Kill clients first
    kill "$CLIENT1_PID" "$CLIENT2_PID" 2>/dev/null
    wait "$CLIENT1_PID" 2>/dev/null
    wait "$CLIENT2_PID" 2>/dev/null
    sleep 0.5
    echo "Clients shut down. Now shutting down the server..."

    # Then kill the server
    kill "$SERVER_PID" 2>/dev/null
    wait "$SERVER_PID" 2>/dev/null
    sleep 2
    echo "Server shut down."
    exit 0
}

# Trap SIGINT signal (Ctrl+C) and call cleanup function
trap cleanup SIGINT

# Run the server in background
./server &
SERVER_PID=$!
sleep 1

# Run the Python clients in background
{
    echo -e "\n"  # First newline input
    echo -e "\n"  # Second newline input
    echo "usr1"   # Actual input for the client
} | python3 client.py &
CLIENT1_PID=$!
sleep 1

{
    echo -e "\n"  # First newline input
    echo -e "\n"  # Second newline input
    echo "usr2"   # Actual input for the client
} | python3 client.py &
CLIENT2_PID=$!

# Wait for all background processes to finish
wait
