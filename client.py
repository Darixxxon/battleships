import socket

import pygame

import board

def main_client(board, HOST, PORT = 12345):
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, int(PORT)))
    print("Client connected to server")
    client_socket.settimeout(0.1)

    server_rdy = "False"    
    board = board
    
    board.choose_layout()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if server_rdy == "False":
            try:
                client_socket.send("True".encode())
                # Waiting for confirmation from server
                server_rdy = client_socket.recv(1024).decode()
                if server_rdy:
                    print("Serwer jest gotowy!")
                    break
                else:
                    print("Server is not ready...")
            except socket.timeout:
                pass
    
    again_move = False
    enemy_again_move = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # Client attacks
        # When server doeasnt have another move and there is client turn
        if not enemy_again_move and board.whose_turn == 0:
            client_move = board.battle()
            client_move = str(client_move[0]) + str(client_move[1])
            client_socket.send(client_move.encode())
            print("Sent move to server")
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                try:
                    print("Waiting for response from server")
                    hit = client_socket.recv(1024).decode()
                    print("Received response from server")
                    if hit == "True":
                        board.attacked_tiles[int(client_move[0])][int(client_move[1])] = 2
                        again_move = True
                        break
                    else:
                        board.attacked_tiles[int(client_move[0])][int(client_move[1])] = 1
                        again_move = False
                        #Turn change
                        board.make_turn()
                        board.draw_board()
                        break
                except socket.timeout:
                    pass
            
        #Server attacks
        #When client doesnt have another move and there is not client turn
        if not again_move and board.whose_turn == 1:
            try:
                server_move = client_socket.recv(1024).decode()
                print("Received move from server")
                server_move = (int(server_move[0]), int(server_move[1]))
                hit = board.receiving_attack(server_move)
                if hit:
                    client_socket.send("True".encode())
                    print("Sent response")
                    enemy_again_move = True
                else:
                    client_socket.send("False".encode())
                    print("Sent response")
                    #Turn change
                    enemy_again_move = False
                    board.make_turn()
            except socket.timeout:
                pass

    client_socket.close()