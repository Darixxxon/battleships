from board import *
import client
import server

if __name__ == "__main__":
   running = True
   board = Board()

   (type, host, port) = board.start_menu()
   if type == "Server":
      server.main_server(board, host, port)
   elif type == "Client":
      client.main_client(board, host, port)
       
   board.determine_enemy_square_color(0,0)
   pygame.quit()
   quit()