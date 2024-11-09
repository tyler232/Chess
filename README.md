# Chess

This is a chess game where two players can connect to a server and play against each other. The server is written in C, which handles communication between the two players via TCP, while the client uses Python’s PyGame for the game logic and frontend.

## Feature
1. Allows two players to play against each other in real time, with both players able to see each other's moves.

2. If a player gets disconnected within 60 seconds, they can reconnect and rejoin the game.

3. Winning Tracking: When a player wins a game, they score 1 point. In the case of a draw, both players will score 1 point

4. After the game finishes, a new game will start automatically after a short period of time.

5. Sound effect for chess move, the player can turn it on or off

## How it works

1. Server: The server, written in C, runs on a machine and listens for incoming TCP connections from players. It manages the game state, handling each player's move by synchronizing the game board between players. When a player disconnects, the server retains their position for 60 seconds. If a player with the same user ID joins, they are reconnected to the game.

2. Client: The client, written in Python using PyGame, connects to the server and provides the front-end interface. Players can move pieces by clicking on the board, and the client sends these moves to the server, which then sends the move to the other client. The client also handles game logic, such as checkmate, stalemate, check, and determining where a piece can and cannot move. The board updates in real time based on the server's response.

## Getting Started

### Configure the server

```bash
./config.sh
pip install -r requirements.txt
```

Run above lines to configure the server informations and install all the dependencies needed, it will let you enter the ip and port you are using to host the server. 

### Put up the server

```bash
./server
```

Run above line to put the server up, only one server is needed for 2 clients

### Start the Game

```bash
python client.py
```

Run above line to start the game

## License

This project is open-source and licensed under the MIT License.


