from board import *
import client
import server
import pygame

if __name__ == "__main__":
    running = True
    board = Board()

    pygame.init()
    clock = pygame.time.Clock() 

    (type, host, port) = board.start_menu()
    
    if type == "Server":
        server.main_server(board, host, port)
    elif type == "Client":
        client.main_client(board, host, port)
    board.determine_enemy_square_color(0, 0)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
        clock.tick(20)

    pygame.quit()
    quit()
