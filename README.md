# Battleship - Multiplayer Game
This is a two-player battleship game with a graphical interface and real-time multiplayer support via client-server communication. each player places ships on their grid, then takes turns attacking enemy tiles. The game continues until one player has all their ships sunk.

# Players can:

Choose between Server or Client roles from the menu.

Place ships using drag-and-drop and rotate them with the Q key.

Play turn-based battles with real-time feedback on hits/misses.

# Project file structure

├── main.py         - launches the game

├── board.py        - all game logic and rendering using pygame

├── client.py       - logic for the client player (connects to server)

├── server.py       - Logic for the server player 

├── constants.py    - global constants 

├── config.ini      - IP/port configuration for client/server

# Concurrent programming techniques

sockets are used for bidirectional communication between server and client

non-blocking sockets with settimeout() avoid freezing the UI while waiting for data.

game turns are synchronized by exchanging data packets.

# External libraries used

pygame	- gui rendering and event handling

socket	- realtime network communication

configparser	- reading IP and port from config.ini

# Screenshots

# group contributions:

Dariusz Morzuch - responsible for connecting the client to the server and transferring data between them

Jan Pastucha - responsible for game logic

Maksymilian Pek - responsible for fixing errors in program logic and creating graphical interface


