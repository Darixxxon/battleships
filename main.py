from board import *

if __name__ == "__main__":
    running = True

    #(type, host, port) = start_menu()
    #if type == "Server":
    #    server.main_server(host, port)
    #elif type == "Client":
    #    client.main_client(host, port)
    board = Board()
    board.create_positioning_board()
    board.create_ships_to_place()
    #board.create_array_with_player_ships()
    #board.create_array_with_enemy_ships()
    #board.create_playing_board()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Close the game when escape is pressed
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                running = False
            if board.get_game_stage() == "placing":
                board.draw_ships_to_place()
                board.place_ships(event)
                board.show_confirm_button()
                board.confirm_button_pressed(event)
            elif board.get_game_stage() == "battle":
                board.create_playing_board()
                board.draw_player_ships()
            board.select_square(event)
            
            #board.move_ship(event)
            pygame.display.flip()
    pygame.quit()
    quit()