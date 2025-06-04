from board import *
import socket

def main_server(board, HOST, PORT = 12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, int(PORT)))
    server_socket.listen(1)
    print("Server is waiting for connection...")
    
    conn, addr = server_socket.accept()
    print(f"Connected with {addr}")
    conn.settimeout(0.1)
    
    client_rdy = "False"
    board = board
    
    board.choose_layout()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if client_rdy == "False":
            try:
                conn.send("True".encode())
                # Waiting for confirmation from client
                client_rdy = conn.recv(1024).decode()
                if client_rdy:
                    print("Client is ready!")
                    break
                else:
                    print("Client is not ready...")
            except socket.timeout:
                pass

        
    # Client starts first
    board.make_turn()
    again_move = False
    enemy_again_move = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # Client attacks
        # When server doeasnt have another move and there is not server turn
        if not again_move and board.whose_turn == 1:
            try:
                #Waiting for move from client
                client_move = conn.recv(1024).decode()
                print("Received move from client")
                client_move = (int(client_move[0]), int(client_move[1]))
                #Check if the move is hit
                hit = board.receiving_attack(client_move)
                if hit == True:
                    conn.send("True".encode())
                    print("Answer sent")
                    enemy_again_move = True
                else:
                    conn.send("False".encode())
                    print("Answer sent")
                    #Turn change
                    board.make_turn()
                    enemy_again_move = False
            except socket.timeout:
                pass
            
        # Server attacks
        # When server has another move and there is server turn
        if not enemy_again_move and board.whose_turn == 0:
            server_move = board.battle()
            server_move = str(server_move[0]) + str(server_move[1])
            print("Sending move to client")
            conn.send(server_move.encode())
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                try:
                    print("Waiting for answer from client...")
                    hit = conn.recv(1024).decode()
                    print("Received answer")
                    if hit == "True":
                        board.attacked_tiles[int(server_move[0])][int(server_move[1])] = 2
                        again_move = True
                        break
                    else:
                        board.attacked_tiles[int(server_move[0])][int(server_move[1])] = 1
                        again_move = False
                        #Turn change
                        board.make_turn()
                        board._redraw_all()
                        break
                except socket.timeout:
                    pass 

    conn.close()
    server_socket.close()