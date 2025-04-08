import socket

import board

def main_client(HOST, PORT = 12345):
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, int(PORT)))
    print("Połączono z serwerem!")

    server_rdy = False
    client_rdy = False
    client_board = None
    
    while True:
        if not client_rdy and type(client_board = board.choose_layout()) == type(list()):
            client_rdy = True
        if client_rdy and not server_rdy:
            client_socket.send(True.encode())
            # Oczekuj na potwierdzenie od klienta
            client_rdy = client_socket.recv(1024).decode()
            if client_rdy:
                print("Klient gotowy!")
                break
            else:
                print("Klient nie jest gotowy, czekam na potwierdzenie...")
        
    while True:
        # Pobierz ruch od klienta
        client_move = input("Twój ruch: ")
        client_socket.send(client_move.encode())

        if client_move == "quit":
            print("Zakończono grę.")
            break

        # Odbierz ruch od serwera
        move = client_socket.recv(1024).decode()
        if move == "quit":
            print("Serwer zakończył grę.")
            break
        print(f"Serwer: {move}")

    client_socket.close()