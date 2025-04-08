import socket

import board

def main_server(HOST, PORT = 12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, int(PORT)))
    server_socket.listen(1)
    print("Serwer czeka na połączenie...")
    
    conn, addr = server_socket.accept()
    print(f"Połączono z {addr}")
    
    server_rdy = False
    client_rdy = False
    server_board = None
    
    while True:
        if not server_rdy and type(server_board = board.choose_layout()) == type(list()):
            server_rdy = True
        if server_rdy and not client_rdy:
            conn.send(True.encode())
            # Oczekuj na potwierdzenie od klienta
            client_rdy = conn.recv(1024).decode()
            if client_rdy:
                print("Klient gotowy!")
                break
            else:
                print("Klient nie jest gotowy, czekam na potwierdzenie...")

        


    while True:
        # Odbierz ruch od klienta
        move = conn.recv(1024).decode()
        if move == "quit":
            print("Klient zakończył grę.")
            break
        print(f"Klient: {move}")

        # Pobierz ruch od serwera
        server_move = input("Twój ruch: ")
        conn.send(server_move.encode())

        if server_move == "quit":
            print("Zakończono grę.")
            break

    conn.close()
    server_socket.close()

