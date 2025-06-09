# Battleship - multiplayer game
This is a two-player battleship game with a graphical interface and real-time multiplayer support via client-server communication. each player places ships on their grid, then takes turns attacking enemy tiles. The game continues until one player has all their ships sunk

# Players can:

Choose between Server or Client roles from the menu.

Place ships and rotate them with the Q key.

Play turn-based battles with real-time feedback on hits/misses.

# Project file structure

main.py         - launches the game

board.py        - all game logic and rendering using pygame

client.py       - logic for the client player (connects to server)

server.py       - Logic for the server player 

constants.py    - global constants 

config.ini      - IP/port configuration for client/server

# Concurrent programming techniques

sockets are used for bidirectional communication between server and client

non-blocking sockets with settimeout() avoid freezing the UI while waiting for data.

# External libraries used

pygame	- gui rendering and event handling

socket	- realtime network communication

configparser	- reading IP and port from config.ini

# Screenshots

initial interface, user can choose between server and client:
![image](https://github.com/user-attachments/assets/82149eb0-0765-4584-bde7-b9f77dc7be46)

after entering two players, each of them can place ships on a board: 
![image](https://github.com/user-attachments/assets/16e68de0-6394-455e-8625-163dba7328f1)

when user put all ships, there is a message whether user is ready to start the game: 
![image](https://github.com/user-attachments/assets/5398d7e0-e62c-4a09-a597-0efa136744bc)

after two confirmations, the battleship is started, on a left user has its own grid, and on a right it has a clear grid, after choose specific cell it can 'shoot' on this cell, assuming that there is a enemy's ship:
![image](https://github.com/user-attachments/assets/354b08b8-d230-46d1-ba3e-df251d641f81)

if user miss the chance, the board is showing his own board, and the turn is changed, enemy has a chance to drown the ship:
![image](https://github.com/user-attachments/assets/3efe8edd-e72e-493d-849d-73787b428e3c)

but if the user hit the enemy's ship the cell is seen as a circle and the user has next chance to 'shoot'. as we can see on a picture, user also see his own grid and the enemy attempts:
![image](https://github.com/user-attachments/assets/4b1b0b17-a02f-421d-942b-670b1f0551d9)

after the all ships are drown there is a on a screen: 
![image](https://github.com/user-attachments/assets/ee6a2d54-8e21-4477-bb71-dec005a3162c)







# group contributions:

Dariusz Morzuch - responsible for connecting the client to the server and transferring data between them

Jan Pastucha - responsible for game logic

Maksymilian Pek - responsible for fixing errors in program logic and creating graphical interface


