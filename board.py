import pygame
import configparser

import random

from constants import ATTACK_BUTTON_X, ATTACK_BUTTON_Y, CONFIRM_BUTTON_X, CONFIRM_BUTTON_Y, BACKGROUND_COLOR, TOTAL_SHIPS, NUMBER_OF_DESTORYES, NUMBER_OF_SUBMARINES, NUMBER_OF_BATTLESHIPS, NUMBER_OF_CARRIERS, NUMBER_OF_CRUISERS, SHIPS, SCREEN_HEIGHT, SCREEN_WIDTH, RECT_WIDTH, RECT_HEIGHT, NUMBER_OF_RECTS, LEFT_MARGIN, TOP_MARGIN, DISTANCE_BETWEEN_BOARDS, ALPHABET

class Board():

    def __init__(self):
        self.whose_turn = 0
        self.player_squares_left_top_corners = []
        self.row = []
        self.enemy_squares_left_top_corners = []
        self.active_box = None
        self.picked_up_color = 0
        self.pickup_height = 0
        self.pickup_segment = 0
        self.ships = {}
        self.placing_ships = True  # Do zmiany na True jak bedziemy odpalac ukladanie
        self.ships_to_place = []
        self.placing_squares_left_top_corners = []
        self.placed_ships = []
        self.side_bounds = []
        self.upper_and_lower_bounds = []
        self.last_valid_position = ()
        self.occupancy_grid = [[0 for _ in range(NUMBER_OF_RECTS)] 
                            for _ in range(NUMBER_OF_RECTS)]
        self.all_ships_placed = False
        self.confirm_button = None
        self.attack_button = None
        self.game_stage = "placing" # Do zmiany na "placing" albo "menu"
        self.placed_ships_coordinates = []
        self.sunken_ships = []
        self.attacked_tiles = [[0 for _ in range(NUMBER_OF_RECTS)] 
                            for _ in range(NUMBER_OF_RECTS)]
        self.enemy_attacked_tiles = [[0 for _ in range(NUMBER_OF_RECTS)]
                            for _ in range(NUMBER_OF_RECTS)]
        self.chosen_tile = ()
        self.enemy_squares_rects = []
        self.enemy_ships = [[random.randint(0, 1) for _ in range(NUMBER_OF_RECTS)] 
                       for _ in range(NUMBER_OF_RECTS)]
        self.enemy_ships[0][0] = 1
        self.enemy_ships[0][1] = 1
        self.enemy_ships[1][0] = 0
        self.selected_tiles = [[0 for _ in range(NUMBER_OF_RECTS)] 
                            for _ in range(NUMBER_OF_RECTS)]
        
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Battle ships")
        self.clock = pygame.time.Clock()
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        #self.background = pygame.image.load("battleships/background.jpg")
        
        
    # Create a surface with given width, height and color
    def surface_create(self, w, h, color=(255, 255, 255)):
        surface = pygame.Surface((w, h))
        surface.fill(color)
        return surface

    # Create a text surface with given text, font size and color
    def text_create(self, text, font_size=36, color=(0, 0, 0)):
        font = pygame.font.SysFont('Arial', font_size)
        return font.render(text, True, color) 

    # Create a rectangle with given coordinates, width, height and color
    def rect_create(self, x, y, w, h, color=(255, 255, 255)):
        
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, color, rect)
        return rect

    # Function to create a start menu
    # It allows to choose if you want to play as a server or client
    def start_menu(self):
        server_host_active = False
        server_port_active = False
        client_host_active = False
        client_port_active = False
        server_host_text = ""
        server_port_text = ""
        client_host_text = ""
        client_port_text = ""

        title_surface = self.surface_create(300, 75)
        server_host_surface = self.surface_create(300, 75)
        server_port_surface = self.surface_create(300, 75)
        server_choose_surface = self.surface_create(200, 75)
        
        client_host_surface = self.surface_create(300, 75)
        client_port_surface = self.surface_create(300, 75)
        client_choose_surface = self.surface_create(200, 75)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if server_host_surface.get_rect(center=(375, 350)).collidepoint(event.pos):
                        server_host_active = True
                    else:
                        server_host_active = False
                        
                    if server_port_surface.get_rect(center=(375, 450)).collidepoint(event.pos):
                        server_port_active = True
                    else:
                        server_port_active = False
                        
                    if server_choose_surface.get_rect(center=(375, 550)).collidepoint(event.pos):
                        return ("Server", server_host_text if server_host_text != "" else self.config.get('SERVER', 'HOST_IP'), server_port_text if server_port_text != "" else self.config.get('SERVER', 'HOST_PORT'))
                    
                        
                    if client_host_surface.get_rect(center=(1125, 350)).collidepoint(event.pos):
                        client_host_active = True
                    else:
                        client_host_active = False
                        
                    if client_port_surface.get_rect(center=(1125, 450)).collidepoint(event.pos):
                        client_port_active = True
                    else:
                        client_port_active = False
                        
                    if client_choose_surface.get_rect(center=(1125, 550)).collidepoint(event.pos):
                        return ("Client", client_host_text if client_host_text != "" else self.config.get('CLIENT', 'HOST_IP'), client_port_text if client_port_text != "" else self.config.get('CLIENT', 'HOST_PORT'))
                
                if event.type == pygame.KEYDOWN and server_host_active:
                    if event.key == pygame.K_BACKSPACE:
                        server_host_text = server_host_text[:-1]
                    else:
                        server_host_text += event.unicode
                    
                if event.type == pygame.KEYDOWN and server_port_active:
                    if event.key == pygame.K_BACKSPACE:
                        server_port_text = server_port_text[:-1]
                    else:
                        server_port_text += event.unicode

                if event.type == pygame.KEYDOWN and client_host_active:
                    if event.key == pygame.K_BACKSPACE:
                        client_host_text = client_host_text[:-1]
                    else:
                        client_host_text += event.unicode
                    
                if event.type == pygame.KEYDOWN and client_port_active:
                    if event.key == pygame.K_BACKSPACE:
                        client_port_text = client_port_text[:-1]
                    else:
                        client_port_text += event.unicode
        
            #self.screen.blit(self.background, (0, 0))
            self.screen.fill((0, 0, 0))
            self.screen.blit(title_surface, title_surface.get_rect(center=(750, 150)))
            self.screen.blit(self.text_create("Choose your role"), self.text_create("Choose your function").get_rect(center=(790, 150)))
            
            self.screen.blit(self.surface_create(200, 75), self.surface_create(200, 75).get_rect(center=(375, 250)))
            self.screen.blit(self.text_create("Server"), self.text_create("Server").get_rect(center=(375, 250)))
            
            self.screen.blit(server_host_surface, server_host_surface.get_rect(center=(375, 350)))
            self.screen.blit(self.text_create("HOST:"), self.text_create("HOST:").get_rect(center=(285, 350)))
            self.screen.blit(self.text_create(server_host_text), self.text_create(server_host_text).get_rect(midleft=(325, 350)))
            
            self.screen.blit(server_port_surface, server_port_surface.get_rect(center=(375, 450)))
            self.screen.blit(self.text_create("PORT:"), self.text_create("PORT:").get_rect(center=(285, 450)))
            self.screen.blit(self.text_create(server_port_text), self.text_create(server_port_text).get_rect(midleft=(325, 450)))
            
            self.screen.blit(server_choose_surface, server_choose_surface.get_rect(center=(375, 550)))
            self.screen.blit(self.text_create("Choose"), self.text_create("Choose").get_rect(center=(375, 550)))
            
            
            
            self.screen.blit(self.surface_create(200, 75), self.surface_create(200, 75).get_rect(center=(1125, 250)))
            self.screen.blit(self.text_create("Client"), self.text_create("Client").get_rect(center=(1125, 250)))
            
            self.screen.blit(client_host_surface, client_host_surface.get_rect(center=(1125, 350)))
            self.screen.blit(self.text_create("HOST:"), self.text_create("HOST:").get_rect(center=(1035, 350)))
            self.screen.blit(self.text_create(client_host_text), self.text_create(client_host_text).get_rect(midleft=(1075, 350)))
            
            self.screen.blit(client_port_surface, client_port_surface.get_rect(center=(1125, 450)))
            self.screen.blit(self.text_create("PORT:"), self.text_create("PORT:").get_rect(center=(1035, 450)))
            self.screen.blit(self.text_create(client_port_text), self.text_create(client_port_text).get_rect(midleft=(1075, 450)))
            
            self.screen.blit(client_choose_surface, client_choose_surface.get_rect(center=(1125, 550)))
            self.screen.blit(self.text_create("Choose"), self.text_create("Choose").get_rect(center=(1125, 550)))
            

            
            pygame.display.update()
            self.clock.tick(20)
    
    # Get the game stage
    def get_game_stage(self):
        return self.game_stage

    # Choosing the layout of the ships
    def choose_layout(self): 
        self.screen.fill((0, 0, 0))  # Tylko raz na początku

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # Close the game when escape is pressed
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.QUIT:
                    running = False
                if self.get_game_stage() == "placing":
                    self.create_positioning_board()
                    self.create_ships_to_place()
                    self.draw_ships_to_place()
                    self.place_ships(event)
                    self.show_confirm_button()
                    self.confirm_button_pressed(event)
                
                # Zaktualizuj planszę po zakończeniu fazy rozmieszczania statków
                pygame.display.flip()  # Tylko po rzeczywistej zmianie

          
    #TODO dodac funkcję która rysuje ataki przeciwnika
    def draw_enemy_hits(self):
        # self.enemy_attacked_tiles

        pygame.display.flip()
     
    # Function to draw board           
    def draw_board(self):
    # Sprawdzenie, czy plansza wymaga odświeżenia
        self.create_playing_board()
        self.draw_player_ships()
        self.draw_enemy_hits()

    # Płynne odświeżanie tylko raz po zmianach
    #pygame.display.flip()  # Zamiast pygame.display.update(), bo flip aktualizuje cały ekran

    
    # Function with mechanic of attacking 
    def battle(self):
        self.screen.fill((0, 0, 0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # Close the game when escape is pressed
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.QUIT:
                    running = False
                if self.get_game_stage() == "battle":
                    self.draw_board()
                    self.select_square(event)
                    self.show_attack_button()
                    pressed = self.attack_button_pressed(event)
                    if pressed:
                        return(pressed[1], pressed[2])
                
                pygame.display.flip()   

    # Create a board at which player can place his/her ships
    def create_positioning_board(self):
        # Set all bounds and left_top_cornerns arrays to be empty so they dont contain multiple copies of same data
        self.upper_and_lower_bounds = []
        self.side_bounds = []
        self.placing_squares_left_top_corners = []
        for i in range(NUMBER_OF_RECTS):
            # Calculate coordiantes of a letter and draw it to the left of the board
            letter_x = SCREEN_WIDTH // 2 - RECT_WIDTH * NUMBER_OF_RECTS // 2 - RECT_WIDTH
            letter_y = TOP_MARGIN // 2 + i * (RECT_HEIGHT) + RECT_HEIGHT // 2
            letter_surface = self.text_create(ALPHABET[i], 24, "white")
            self.screen.blit(letter_surface, (letter_x, letter_y))

            self.row = []

            for j in range(NUMBER_OF_RECTS):
                # Calculate rect position and draw it to the screen
                rect_x = SCREEN_WIDTH // 2 - RECT_WIDTH * NUMBER_OF_RECTS // 2 + j * RECT_WIDTH + j
                rect_y = TOP_MARGIN // 2 + i * RECT_HEIGHT + i
                rect = pygame.Rect(rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT)
                pygame.draw.rect(self.screen, "white", rect)
                
                # Add rects coordinates and x,y as tuples to the row array
                self.row.append([(i, j), (rect_x, rect_y)])
                # Check if the first row of board is currently being drawn
                if (i == 0):
                    # Calculate coordiantes of a number and draw it at the top of the board
                    number_x = SCREEN_WIDTH // 2 - RECT_WIDTH * NUMBER_OF_RECTS // 2 + j * (RECT_WIDTH + 1) + RECT_WIDTH // 2
                    number_y = TOP_MARGIN // 2 - 40
                    number_surface = self.text_create(str(j+1), 24, "white")
                    self.screen.blit(number_surface, (number_x, number_y))
                
                # Add left bound and top bound to the bounds arrays    
                if (i == 0 and j == 0):
                    self.upper_and_lower_bounds.append(rect_y)
                    self.side_bounds.append(rect_x)
                # Add right bound and lower bound to the bounds arrays
                if (i == NUMBER_OF_RECTS - 1 and j == NUMBER_OF_RECTS - 1):
                    self.upper_and_lower_bounds.append(rect_y + RECT_HEIGHT)
                    self.side_bounds.append(rect_x + RECT_WIDTH)
            self.placing_squares_left_top_corners.append(self.row)
        pygame.display.flip()

    # Create all ships that are supposed to be available to place
    def create_ships_to_place(self):
        for i in range(TOTAL_SHIPS):
            # Calculate the ships position under the board
            rect_x = SCREEN_WIDTH // 2 - RECT_WIDTH * NUMBER_OF_RECTS // 2 + i * (RECT_WIDTH + 10)
            rect_y = TOP_MARGIN + RECT_HEIGHT * NUMBER_OF_RECTS

            if i < NUMBER_OF_DESTORYES:
                self.create_destroyer_to_place(rect_x, rect_y)
            elif i < NUMBER_OF_DESTORYES + NUMBER_OF_SUBMARINES:
                self.create_submarine_to_place(rect_x, rect_y)
            elif i < NUMBER_OF_DESTORYES + NUMBER_OF_SUBMARINES + NUMBER_OF_CRUISERS:
                self.create_cruiser_to_place(rect_x, rect_y)
            elif i < NUMBER_OF_DESTORYES + NUMBER_OF_SUBMARINES + NUMBER_OF_CRUISERS + NUMBER_OF_BATTLESHIPS:
                self.create_battleship_to_place(rect_x, rect_y)
            else:
                self.create_carrier_to_place(rect_x, rect_y)           
        pygame.display.flip()

    # Draw ships that are present in the ships_to_place array to the board
    def draw_ships_to_place(self):
        for ship in self.ships_to_place:
            pygame.draw.rect(self.screen, ship[1], ship[0])

    # Create a rectangle representing submarine
    def create_submarine_to_place(self, x, y):
        submarine_parameters = SHIPS["submarine"]
        rect = pygame.Rect(x, y, submarine_parameters[2], submarine_parameters[1])
        self.ships_to_place.append([rect, submarine_parameters[0]])  

    # Create a rectangle representing destroyer
    def create_destroyer_to_place(self, x, y):
        destoryer_parameters = SHIPS["destroyer"]
        rect = pygame.Rect(x, y, destoryer_parameters[2], destoryer_parameters[1])
        self.ships_to_place.append([rect, destoryer_parameters[0]])     

    # Create a rectangle representing cruiser
    def create_cruiser_to_place(self, x, y):
        cruiser_parameters = SHIPS["cruiser"]
        rect = pygame.Rect(x, y, cruiser_parameters[2], cruiser_parameters[1])
        self.ships_to_place.append([rect, cruiser_parameters[0]])  

    # Create a rectangle representing battleship
    def create_battleship_to_place(self, x, y):
        battleship_parameters = SHIPS["battleship"]
        rect = pygame.Rect(x, y, battleship_parameters[2], battleship_parameters[1])
        self.ships_to_place.append([rect, battleship_parameters[0]])  

    # Create a rectangle representing carrier
    def create_carrier_to_place(self, x, y):
        carrier_parameters = SHIPS["carrier"]
        rect = pygame.Rect(x, y, carrier_parameters[2], carrier_parameters[1])
        self.ships_to_place.append([rect, carrier_parameters[0]])  

    # Determine at which square is the ship located
    def determine_square(self, x, y):
        squares_left_top_corners = []
        found_height = False 
        found_width = False
        found_x = 0
        found_y = 0
        
        if self.placing_ships: # Assign different coordinate arrays based on the stage of the game
            squares_left_top_corners = self.placing_squares_left_top_corners
        else:
            squares_left_top_corners = self.enemy_squares_left_top_corners
             
        if (not (self.side_bounds[0] <= x < self.side_bounds[1])) and (not (self.upper_and_lower_bounds[0] <= y < self.upper_and_lower_bounds[1])): 
            # Check if the square is within bounds
            return -1 
          
        if len(squares_left_top_corners) < NUMBER_OF_RECTS:
            return -1  
          
        if not found_height or not found_width:
            for i in range(NUMBER_OF_RECTS):
                top_border = squares_left_top_corners[i][0][1][1]
                bottom_border = top_border + RECT_HEIGHT

                if top_border <= y < bottom_border:
                    found_height = True
                    found_x = i
                if not found_width:
                    for j in range(NUMBER_OF_RECTS):
                        left_border = squares_left_top_corners[0][j][1][0]
                        right_border = left_border + RECT_WIDTH
                        if left_border <= x < right_border:
                            found_width = True
                            found_y = j
        return (found_x, found_y)
    
    # Placing, moving and rotating ships
    def place_ships(self, event):
        if event.type == pygame.KEYDOWN:
            # Rotate the active ship on q button pressed
            if event.key == pygame.K_q and self.active_box is not None:
                ship_rect = self.ships_to_place[self.active_box][0]
                # Swap width and height
                ship_rect.width, ship_rect.height = ship_rect.height, ship_rect.width
                # Adjust position to keep the same center point
                ship_rect.x -= (ship_rect.height - ship_rect.width) // 2
                ship_rect.y -= (ship_rect.width - ship_rect.height) // 2
                self.redraw_all()
                return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # First check if we're clicking on an already placed ship
                for num, box in enumerate(self.placed_ships):
                    if box[0].collidepoint(event.pos):
                        self.active_box = num
                        self.picked_up_color = box[1]
                        self.last_valid_position = box[0].topleft
                        
                        # Calculate which segment of the ship was clicked
                        ship_rect = box[0]
                        click_y = event.pos[1] - ship_rect.y
                        ship_height = ship_rect.height
                        
                        # Calculate segment height (each segment is 1 unit tall)
                        segment = min(int(click_y / RECT_HEIGHT), ship_height - 1)
                        self.pickup_segment = segment
                        
                        self.ships_to_place.append(self.placed_ships.pop(num))
                        break
                # Check ships_to_place
                else:
                    for num, box in enumerate(self.ships_to_place):
                        if box[0].collidepoint(event.pos):
                            self.active_box = num
                            self.picked_up_color = box[1]
                            self.last_valid_position = box[0].topleft
                            
                            # Calculate which segment of the ship was clicked
                            ship_rect = box[0]
                            click_y = event.pos[1] - ship_rect.y
                            ship_height = ship_rect.height
                            
                            # Calculate segment height (each segment is 1 unit tall)
                            segment = min(int(click_y / RECT_HEIGHT), ship_height - 1)
                            self.pickup_segment = segment
                            
                            break
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.active_box is not None:
                square = self.determine_square(event.pos[0], event.pos[1])
                if square != -1:
                    y, x = square  # grid coordinates
                    moving_ship = self.ships_to_place[self.active_box]
                    ship_rect = moving_ship[0]
                    ship_height = ship_rect.height
                    ship_width = ship_rect.width
                    
                    # Determine orientation (vertical if height > width)
                    is_vertical = ship_height > ship_width
                    
                    if is_vertical:
                        # Vertical placement logic
                        actual_top_y = y - self.pickup_segment
                        
                        # Validate placement
                        valid_placement = True
                        for i in range(int(ship_height // RECT_HEIGHT)):
                            check_y = actual_top_y + i
                            if (check_y < 0 or check_y >= len(self.occupancy_grid) or 
                                self.occupancy_grid[check_y][x] > 0):
                                valid_placement = False
                                break
                        
                        if valid_placement:
                            # Calculate new position
                            new_x = self.placing_squares_left_top_corners[0][x][1][0]
                            new_y = self.placing_squares_left_top_corners[y][0][1][1] - (self.pickup_segment * RECT_HEIGHT)
                            
                            # Boundary checking
                            new_y = max(self.upper_and_lower_bounds[0], 
                                    min(new_y, self.upper_and_lower_bounds[1] - ship_height))
                            
                            # Update ship position
                            ship_rect.topleft = (new_x, new_y)
                            self.last_valid_position = (new_x, new_y)
                            
                            # Add to placed ships
                            self.placed_ships.append(moving_ship)
                            self.ships_to_place.pop(self.active_box)
                            self.add_occupied()
                            self.check_if_all_ships_were_placed()
                        else:
                            # Return to last valid position if placement is invalid
                            ship_rect.topleft = self.last_valid_position
                            
                    else:
                        # Horizontal placement logic
                        actual_left_x = x - self.pickup_segment
                        
                        # Validate placement
                        valid_placement = True
                        for i in range(int(ship_width // RECT_WIDTH)):
                            check_x = actual_left_x + i
                            if (check_x < 0 or check_x >= len(self.occupancy_grid[0]) or 
                                self.occupancy_grid[y][check_x] > 0):
                                valid_placement = False
                                break
                        
                        if valid_placement:
                            # Calculate new position
                            new_x = self.placing_squares_left_top_corners[0][actual_left_x][1][0]
                            new_y = self.placing_squares_left_top_corners[y][0][1][1]
                            
                            # Boundary checking
                            new_x = max(self.side_bounds[0],
                                    min(new_x, self.side_bounds[1] - ship_width))
                            
                            # Update ship position
                            ship_rect.topleft = (new_x, new_y)
                            self.last_valid_position = (new_x, new_y)
                            
                            # Add to placed ships
                            self.placed_ships.append(moving_ship)
                            self.ships_to_place.pop(self.active_box)
                            self.add_occupied()
                            self.check_if_all_ships_were_placed()
                        else:
                            # Return to last valid position if placement is invalid
                            ship_rect.topleft = self.last_valid_position
                            
                else:
                    # Return to last valid position if not over a valid square
                    self.ships_to_place[self.active_box][0].topleft = self.last_valid_position
                
                # Reset active box
                self.active_box = None
                self.redraw_all()

        if event.type == pygame.MOUSEMOTION:
            if self.active_box is not None:
                self.redraw_all()
                self.ships_to_place[self.active_box][0].move_ip(event.rel)
                pygame.draw.rect(self.screen, self.picked_up_color, 
                            self.ships_to_place[self.active_box][0])
                pygame.display.flip()
   
    # Add ships' and neighbouring squares to the occupancy table
    def add_occupied(self):
        # Check what ship was placed last
        latest_ship = self.placed_ships[-1][0]
        
        # Find which square is ships top left part occupying
        ship_squares = self.determine_square(latest_ship.x, latest_ship.y)
        
        if ship_squares == -1:
            return
        
        ship_x, ship_y = ship_squares
        ships_id = self.determine_ship_id(self.placed_ships[-1][1])
        
        # Check if ship is vertical or horizontal
        is_vertical = latest_ship.height > latest_ship.width
        
        if is_vertical:
            ship_height_squares = int(latest_ship.height // RECT_HEIGHT)
            ship_width_squares = 1
        else:
            ship_height_squares = 1
            ship_width_squares = int(latest_ship.width // RECT_WIDTH)
        # Mark ship squares and their neighbors
        for i in range(-1, ship_height_squares + 1):
            for j in range(-1, ship_width_squares + 1):
                current_x = ship_x + i
                current_y = ship_y + j
                
                if (current_x < 0 or current_y < 0 or 
                    current_x >= len(self.occupancy_grid) or 
                    current_y >= len(self.occupancy_grid[0])):
                    continue
                
                if 0 <= i < ship_height_squares and 0 <= j < ship_width_squares:
                    self.occupancy_grid[current_x][current_y] = ships_id
                elif self.occupancy_grid[current_x][current_y] == 0:
                    self.occupancy_grid[current_x][current_y] = 9
     
    # Check if all ships that are supposed to be placed were placed    
    def check_if_all_ships_were_placed(self):
        if TOTAL_SHIPS == len(self.placed_ships):
            self.all_ships_placed = True
        
    # Function to show the button that confirms the placement of ships 
    def show_confirm_button(self):
        if self.all_ships_placed:
            button = pygame.rect.Rect(CONFIRM_BUTTON_X,  CONFIRM_BUTTON_Y, RECT_WIDTH * 3, RECT_HEIGHT * 1.5)
            pygame.draw.rect(self.screen, "gray", button)
            
            text_x = SCREEN_WIDTH // 2 - RECT_WIDTH * 1.5
            text_y = TOP_MARGIN + RECT_HEIGHT * NUMBER_OF_RECTS
            text_surface = self.text_create("CONFIRM", 24, "black")
            self.screen.blit(text_surface, (text_x, text_y))
            
            self.confirm_button = button
            
            pygame.display.flip()  
       
    # Detect if confirm button was pressed    
    def confirm_button_pressed(self, event):
        if self.confirm_button is not None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.confirm_button.collidepoint(event.pos):
                        print("Confirm button pressed")
                        for ship in self.placed_ships:
                            ship_coordinates = self.determine_square(ship[0].x, ship[0].y)
                            self.placed_ships_coordinates.append((ship, ship_coordinates))
                        print(self.placed_ships_coordinates)
                        self.game_stage = "battle"
                        self.placing_ships = False
                        self.screen.fill(BACKGROUND_COLOR)

                    return
                
        return
        
    # Check what is the id of the ship, so it can be placed in the occupancy grid        
    def determine_ship_id(self, color):
        for key, value in SHIPS.items():
            if value[0] == color:
                return value[3]
        return -1
    
    # Redraw eveyrthing to the screen
    def redraw_all(self):
        self.screen.fill(BACKGROUND_COLOR)
        #self.screen.blit(self.background, (0, 0))
        self.screen.fill((0, 0, 0))
        self.create_positioning_board()
        # Draw placed ships first
        for ship in self.placed_ships:
            pygame.draw.rect(self.screen, ship[1], ship[0])
        # Then draw ships waiting to be placed
        for i, ship in enumerate(self.ships_to_place):
            if i != self.active_box:  # Don't draw the active ship here
                pygame.draw.rect(self.screen, ship[1], ship[0])
        pygame.display.flip()

    # Function to create two basic boards with letters and numbers representing coordinates written next to them      
    def create_playing_board(self):
        self.player_squares_left_top_corners = []
        self.upper_and_lower_bounds = []
        self.side_bounds = []
        # Create board for first player
        for i in range(NUMBER_OF_RECTS):
            letter_x = LEFT_MARGIN - 30
            letter_y = TOP_MARGIN + i * (RECT_HEIGHT) + RECT_HEIGHT // 2
            letter_surface = self.text_create(ALPHABET[i], 24, "white")
            self.screen.blit(letter_surface, (letter_x, letter_y))

            self.row = []

            for j in range(NUMBER_OF_RECTS):
                rect_x = LEFT_MARGIN + j * RECT_WIDTH + j
                rect_y = TOP_MARGIN + i * RECT_HEIGHT + i
                rect = pygame.Rect(rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT)
                pygame.draw.rect(self.screen, "white", rect)
                self.row.append([(i, j), (rect_x, rect_y)])
                if (i == 0):
                    number_x = LEFT_MARGIN + j * (RECT_WIDTH + 1) + RECT_WIDTH // 2
                    number_y = TOP_MARGIN - 40
                    number_surface = self.text_create(str(j+1), 24, "white")
                    self.screen.blit(number_surface, (number_x, number_y))
                
                # Add left bound and top bound to the bounds arrays    
                if (i == 0 and j == 0):
                    self.upper_and_lower_bounds.append(rect_y)
                    self.side_bounds.append(rect_x)
                # Add right bound and lower bound to the bounds arrays
                if (i == NUMBER_OF_RECTS - 1 and j == NUMBER_OF_RECTS - 1):
                    self.upper_and_lower_bounds.append(rect_y + RECT_HEIGHT)
                    self.side_bounds.append(rect_x + RECT_WIDTH)
            self.player_squares_left_top_corners.append(self.row)
            
        # Create board for second player
        for i in range(NUMBER_OF_RECTS):
            self.row = []
            self.rect_row = []
            letter_x = LEFT_MARGIN - 30 + DISTANCE_BETWEEN_BOARDS + NUMBER_OF_RECTS * RECT_WIDTH
            letter_y = TOP_MARGIN + i * (RECT_HEIGHT) + RECT_HEIGHT // 2
            letter_surface = self.text_create(ALPHABET[i], 24, "white")
            self.screen.blit(letter_surface, (letter_x, letter_y))
            for j in range(NUMBER_OF_RECTS):
                rect_x = LEFT_MARGIN + j * RECT_WIDTH + j + DISTANCE_BETWEEN_BOARDS + NUMBER_OF_RECTS * RECT_WIDTH
                rect_y = TOP_MARGIN + i * RECT_HEIGHT + i
                rect = pygame.Rect(rect_x, rect_y , RECT_WIDTH, RECT_HEIGHT)
                self.determine_enemy_square_color(rect_x, rect_y)
                self.row.append([(i, j), (rect_x, rect_y)])
                if len(self.enemy_squares_rects) < NUMBER_OF_RECTS ** 2:
                    self.enemy_squares_rects.append(rect)

                if (i == 0):
                    number_x = LEFT_MARGIN + j * (RECT_WIDTH + 1) + DISTANCE_BETWEEN_BOARDS + NUMBER_OF_RECTS * RECT_WIDTH + RECT_WIDTH // 2
                    number_y = TOP_MARGIN - 40
                    number_surface = self.text_create(str(j+1), 24, "white")
                    self.screen.blit(number_surface, (number_x, number_y))
            if len(self.enemy_squares_left_top_corners) < NUMBER_OF_RECTS:
                self.enemy_squares_left_top_corners.append(self.row)

        turn_x = SCREEN_WIDTH // 2 - 100
        turn_y = TOP_MARGIN - 75
        if self.whose_turn == 0:
            turn_surface = self.text_create("Your turn", 36, "white")
        else:
            turn_surface = self.text_create("Enemy turn", 36, "white")
        self.screen.blit(turn_surface, (turn_x, turn_y))

        pygame.display.flip()

    # Determine at which cooridantes is the square located
    def determine_coordinates(self, x, y):
        return self.player_squares_left_top_corners[x][y][1]

    # Function to draw ships to the player board
    def draw_player_ships(self):

        for ship in self.placed_ships_coordinates:
            rect = ship[0][0]
            ship_color = ship[0][1]
            ship_coordinates = ship[1]
            
            new_position = self.determine_coordinates(ship_coordinates[0], ship_coordinates[1])
            new_rect = pygame.rect.Rect(new_position[0],new_position[1], rect.width, rect.height)
            
            pygame.draw.rect(self.screen, ship_color, new_rect)

        pygame.display.flip()
    
    # Function to determine what color should be enemy square colored
    def determine_enemy_square_color(self, x, y):
        which_square = self.determine_square(x, y)
        if which_square == -1:
            return "white"
        square_x, square_y = which_square[0], which_square[1]
        
        # Draw the base white square
        rect = pygame.Rect(x, y, RECT_WIDTH, RECT_HEIGHT)
        pygame.draw.rect(self.screen, "white", rect)
        
        # If selected, highlight with red border
        if self.selected_tiles[square_x][square_y]:
            pygame.draw.rect(self.screen, "red", rect, 2)  # 2 is the border width
        
        # Draw X for miss (attacked_tiles == 1)
        if self.attacked_tiles[square_x][square_y] == 1:
            # Draw an X
            start_pos1 = (x + 5, y + 5)
            end_pos1 = (x + RECT_WIDTH - 5, y + RECT_HEIGHT - 5)
            start_pos2 = (x + RECT_WIDTH - 5, y + 5)
            end_pos2 = (x + 5, y + RECT_HEIGHT - 5)
            pygame.draw.line(self.screen, "red", start_pos1, end_pos1, 2)
            pygame.draw.line(self.screen, "red", start_pos2, end_pos2, 2)
        
        # Draw circle for hit (attacked_tiles == 2)
        elif self.attacked_tiles[square_x][square_y] == 2:
            center = (x + RECT_WIDTH // 2, y + RECT_HEIGHT // 2)
            radius = RECT_WIDTH // 2 - 5
            pygame.draw.circle(self.screen, "red", center, radius, 2)
        
        return None  # We're doing the drawing here, so no need to return a color
    
    # Function to select squares on enemy board
    def select_square(self, event):
        if self.whose_turn == 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for box in self.enemy_squares_rects:
                        if box.collidepoint(event.pos):
                            which_square = self.determine_square(event.pos[0], event.pos[1])
                            square_x, square_y = which_square[0], which_square[1]
                            self.selected_tiles = [[0 for _ in range(NUMBER_OF_RECTS)] 
                                for _ in range(NUMBER_OF_RECTS)]
                            self.selected_tiles[square_x][square_y] = 1

    # Function to show the button that confirms the placement of ships 
    def show_attack_button(self):
        if self.whose_turn == 0:
            button = pygame.rect.Rect(ATTACK_BUTTON_X, ATTACK_BUTTON_Y, RECT_WIDTH * 3, RECT_HEIGHT * 1.5)
            pygame.draw.rect(self.screen, "gray", button)
            
            text_surface = self.text_create("ATTACK", 24, "black")
            self.screen.blit(text_surface, (ATTACK_BUTTON_X, ATTACK_BUTTON_Y))
            
            self.attack_button = button
            
            pygame.display.flip()  
     
    # Function to check if attack button was pressed 
    def attack_button_pressed(self, event):
        x = 99
        y = 99
        if self.whose_turn == 0:
            if self.attack_button is not None:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.attack_button.collidepoint(event.pos):
                            print("Attack button pressed")
                            self.screen.fill(BACKGROUND_COLOR)
                            for i in range(NUMBER_OF_RECTS):
                                for j in range(NUMBER_OF_RECTS):
                                    if self.selected_tiles[i][j] == 1:
                                        x = i
                                        y = j
                            self.selected_tiles = [[0 for _ in range(NUMBER_OF_RECTS)] 
                                for _ in range(NUMBER_OF_RECTS)]
                        if x != 99 and y != 99:
                            return (True, x, y)
                    
            return (False)
     
    #TODO zmienic na lepszą tabelkę
    # Function to check if the attack was successful
    def receiving_attack(self, attack):
        x = attack[0]
        y = attack[1]
        hit = False
        for ships in self.placed_ships_coordinates:
            if ships[1] == (x, y):
                self.enemy_attacked_tiles[x][y] = 2
                hit = True
                break
        if not hit:
            self.enemy_attacked_tiles[x][y] = 1
        return hit
     
    # Switch turns 
    def make_turn(self):
        self.whose_turn = 0 if self.whose_turn == 1 else 1 
        return
