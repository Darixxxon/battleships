import pygame
import configparser

from constants import BACKGROUND_COLOR, TOTAL_SHIPS, NUMBER_OF_DESTORYES, NUMBER_OF_SUBMARINES, NUMBER_OF_BATTLESHIPS, NUMBER_OF_CARRIERS, NUMBER_OF_CRUISERS, SHIPS, SCREEN_HEIGHT, SCREEN_WIDTH, RECT_WIDTH, RECT_HEIGHT, NUMBER_OF_RECTS, LEFT_MARGIN, TOP_MARGIN, DISTANCE_BETWEEN_BOARDS, ALPHABET

import client
import server

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle ships")
clock = pygame.time.Clock()
config = configparser.ConfigParser()
config.read("config.ini")

def surface_create(w, h, color=(255, 255, 255)):
    
    surface = pygame.Surface((w, h))
    surface.fill(color)
    return surface

def text_create(text, font_size=36, color=(0, 0, 0)):
    font = pygame.font.SysFont('Arial', font_size)
    return font.render(text, True, color) 

def rect_create(x, y, w, h, color=(255, 255, 255)):
    
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect)
    return rect

def start_menu():
    background = pygame.image.load("background.jpg")
    server_host_active = False
    server_port_active = False
    client_host_active = False
    client_port_active = False
    server_host_text = ""
    server_port_text = ""
    client_host_text = ""
    client_port_text = ""

    title_surface = surface_create(300, 75)
    server_host_surface = surface_create(300, 75)
    server_port_surface = surface_create(300, 75)
    server_choose_surface = surface_create(200, 75)
    
    client_host_surface = surface_create(300, 75)
    client_port_surface = surface_create(300, 75)
    client_choose_surface = surface_create(200, 75)

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
                    return ("Server", server_host_text if server_host_text != "" else config.get('SERVER', 'HOST_IP'), server_port_text if server_port_text != "" else config.get('SERVER', 'HOST_PORT'))
                
                    
                if client_host_surface.get_rect(center=(1125, 350)).collidepoint(event.pos):
                    client_host_active = True
                else:
                    client_host_active = False
                    
                if client_port_surface.get_rect(center=(1125, 450)).collidepoint(event.pos):
                    client_port_active = True
                else:
                    client_port_active = False
                    
                if client_choose_surface.get_rect(center=(1125, 550)).collidepoint(event.pos):
                    return ("Client", client_host_text if client_host_text != "" else config.get('CLIENT', 'HOST_IP'), client_port_text if client_port_text != "" else config.get('CLIENT', 'HOST_PORT'))
            
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
    
        screen.blit(background, (0, 0))
        # screen.blit(surface_create(300, 100), (600, 100))
        screen.blit(title_surface, title_surface.get_rect(center=(750, 150)))
        screen.blit(text_create("Choose your function"), text_create("Choose your function").get_rect(center=(750, 150)))
        
        screen.blit(surface_create(200, 75), surface_create(200, 75).get_rect(center=(375, 250)))
        screen.blit(text_create("Server"), text_create("Server").get_rect(center=(375, 250)))
        
        screen.blit(server_host_surface, server_host_surface.get_rect(center=(375, 350)))
        screen.blit(text_create("HOST:"), text_create("HOST:").get_rect(center=(275, 350)))
        screen.blit(text_create(server_host_text), text_create(server_host_text).get_rect(midleft=(325, 350)))
        
        screen.blit(server_port_surface, server_port_surface.get_rect(center=(375, 450)))
        screen.blit(text_create("PORT:"), text_create("PORT:").get_rect(center=(275, 450)))
        screen.blit(text_create(server_port_text), text_create(server_port_text).get_rect(midleft=(325, 450)))
        
        screen.blit(server_choose_surface, server_choose_surface.get_rect(center=(375, 550)))
        screen.blit(text_create("Choose"), text_create("Choose").get_rect(center=(375, 550)))
        
        
        
        screen.blit(surface_create(200, 75), surface_create(200, 75).get_rect(center=(1125, 250)))
        screen.blit(text_create("Client"), text_create("Client").get_rect(center=(1125, 250)))
        
        screen.blit(client_host_surface, client_host_surface.get_rect(center=(1125, 350)))
        screen.blit(text_create("HOST:"), text_create("HOST:").get_rect(center=(1025, 350)))
        screen.blit(text_create(client_host_text), text_create(client_host_text).get_rect(midleft=(1075, 350)))
        
        screen.blit(client_port_surface, client_port_surface.get_rect(center=(1125, 450)))
        screen.blit(text_create("PORT:"), text_create("PORT:").get_rect(center=(1025, 450)))
        screen.blit(text_create(client_port_text), text_create(client_port_text).get_rect(midleft=(1075, 450)))
        
        screen.blit(client_choose_surface, client_choose_surface.get_rect(center=(1125, 550)))
        screen.blit(text_create("Choose"), text_create("Choose").get_rect(center=(1125, 550)))
        

        # screen.fill((255, 255, 255))
        # pygame.display.flip()
        pygame.display.update()
        clock.tick(20)
      
def choose_layout():
    background = pygame.image.load("background.jpg")
    board_layout =[[surface_create(70, 70) for _ in range(10)] for _ in range(10)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(background, (0, 0))
        
        screen.blit(surface_create(300, 75), surface_create(300, 75).get_rect(center=(450, 70)))
        screen.blit(text_create("YOUR BOARD"), text_create("YOUR BOARD").get_rect(center=(450, 70)))
        
        for i in range(10):
            for j in range(10):
                board_layout[i][j].fill((255, 255, 255))
                screen.blit(board_layout[i][j], (i * 70 + 100, j * 70 + 150))
                # rect_create(i * 70 + 100, j * 70 + 100, 70, 70)
        for i in range(11):
            pygame.draw.line(screen, (0, 0, 0), (i * 70 + 100, 150), (i * 70 + 100, 850), 1)
            pygame.draw.line(screen, (0, 0, 0), (100, i * 70 + 150), (800, i * 70 + 150), 1)
            
        screen.blit(surface_create(300, 75), surface_create(300, 75).get_rect(center=(1100, 70)))
        screen.blit(text_create("YOUR SHIPS"), text_create("YOUR SHIPS").get_rect(center=(1100, 70)))
            
        screen.blit(surface_create(70, 280, color=(128, 128, 128)), surface_create(70, 280, color=(128, 128, 128)).get_rect(topleft=(850, 150)))
        
        screen.blit(surface_create(70, 210, color=(128, 128, 128)), surface_create(70, 210, color=(128, 128, 128)).get_rect(topleft=(950, 150)))
        screen.blit(surface_create(70, 210, color=(128, 128, 128)), surface_create(70, 210, color=(128, 128, 128)).get_rect(topleft=(1050, 150)))
        
        screen.blit(surface_create(70, 140, color=(128, 128, 128)), surface_create(70, 140, color=(128, 128, 128)).get_rect(topleft=(1150, 150)))
        screen.blit(surface_create(70, 140, color=(128, 128, 128)), surface_create(70, 140, color=(128, 128, 128)).get_rect(topleft=(1150, 350)))
        screen.blit(surface_create(70, 140, color=(128, 128, 128)), surface_create(70, 140, color=(128, 128, 128)).get_rect(topleft=(1150, 550)))
        
        screen.blit(surface_create(70, 70, color=(128, 128, 128)), surface_create(70, 70, color=(128, 128, 128)).get_rect(topleft=(1250, 150)))
        screen.blit(surface_create(70, 70, color=(128, 128, 128)), surface_create(70, 70, color=(128, 128, 128)).get_rect(topleft=(1250, 250)))
        screen.blit(surface_create(70, 70, color=(128, 128, 128)), surface_create(70, 70, color=(128, 128, 128)).get_rect(topleft=(1250, 350)))
        screen.blit(surface_create(70, 70, color=(128, 128, 128)), surface_create(70, 70, color=(128, 128, 128)).get_rect(topleft=(1250, 450)))
        
        
        pygame.display.update()
        clock.tick(20)  


class Board():

    def __init__(self):
        self.player_board = []
        self.enemy_board = []
        self.whose_turn = 0
        self.board_squares = []
        self.player_squares_left_top_corners = []
        self.row = []
        self.enemy_squares_left_top_corners = []
        self.active_box = None
        self.picked_up_color = 0
        self.pickup_height = 0
        self.pickup_segment = 0
        self.ships = {}
        self.placing_ships = True
        self.ships_to_place = []
        self.placing_squares_left_top_corners = []
        self.placed_ships = []
        self.side_bounds = []
        self.upper_and_lower_bounds = []
        self.last_valid_position = ()
        self.occupancy_grid = [[0 for _ in range(NUMBER_OF_RECTS)] 
                            for _ in range(NUMBER_OF_RECTS)]
        self.all_ships_placed = False

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
            letter_surface = text_create(ALPHABET[i], 24, "white")
            screen.blit(letter_surface, (letter_x, letter_y))

            self.row = []

            for j in range(NUMBER_OF_RECTS):
                # Calculate rect position and draw it to the screen
                rect_x = SCREEN_WIDTH // 2 - RECT_WIDTH * NUMBER_OF_RECTS // 2 + j * RECT_WIDTH + j
                rect_y = TOP_MARGIN // 2 + i * RECT_HEIGHT + i
                rect = pygame.Rect(rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT)
                pygame.draw.rect(screen, "white", rect)
                
                # Add rects coordinates and x,y as tuples to the row array
                self.row.append([(i, j), (rect_x, rect_y)])
                # Check if the first row of board is currently being drawn
                if (i == 0):
                    # Calculate coordiantes of a number and draw it at the top of the board
                    number_x = SCREEN_WIDTH // 2 - RECT_WIDTH * NUMBER_OF_RECTS // 2 + j * (RECT_WIDTH + 1) + RECT_WIDTH // 2
                    number_y = TOP_MARGIN // 2 - 40
                    number_surface = text_create(str(j+1), 24, "white")
                    screen.blit(number_surface, (number_x, number_y))
                
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
            pygame.draw.rect(screen, ship[1], ship[0])

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
            squares_left_top_corners = self.player_squares_left_top_corners
             
        if (not (self.side_bounds[0] <= x < self.side_bounds[1])) and (not (self.upper_and_lower_bounds[0] <= y < self.upper_and_lower_bounds[1])): 
            # Check if the square is within bounds
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
                pygame.draw.rect(screen, self.picked_up_color, 
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
            return True
        return False
    
      
    def show_confirm_button(self):
        if self.all_ships_placed:
            return  
        
    # Check what is the id of the ship, so it can be placed in the occupancy grid        
    def determine_ship_id(self, color):
        for key, value in SHIPS.items():
            if value[0] == color:
                return value[3]
        return -1
    
    # Redraw eveyrthing to the screen
    def redraw_all(self):
        screen.fill(BACKGROUND_COLOR)
        self.create_positioning_board()
        # Draw placed ships first
        for ship in self.placed_ships:
            pygame.draw.rect(screen, ship[1], ship[0])
        # Then draw ships waiting to be placed
        for i, ship in enumerate(self.ships_to_place):
            if i != self.active_box:  # Don't draw the active ship here
                pygame.draw.rect(screen, ship[1], ship[0])
        pygame.display.flip()

    # Function to create two basic boards with letters and numbers representing coordinates written next to them      
    def create_playing_board(self):
        # Create board for first player
        for i in range(NUMBER_OF_RECTS):
            letter_x = LEFT_MARGIN - 30
            letter_y = TOP_MARGIN + i * (RECT_HEIGHT) + RECT_HEIGHT // 2
            letter_surface = text_create(ALPHABET[i], 24, "white")
            screen.blit(letter_surface, (letter_x, letter_y))

            self.row = []

            for j in range(NUMBER_OF_RECTS):
                rect_x = LEFT_MARGIN + j * RECT_WIDTH + j
                rect_y = TOP_MARGIN + i * RECT_HEIGHT + i
                rect = pygame.Rect(rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT)
                pygame.draw.rect(screen, "white", rect)
                self.row.append([(i, j), (rect_x, rect_y)])
                if (i == 0):
                    number_x = LEFT_MARGIN + j * (RECT_WIDTH + 1) + RECT_WIDTH // 2
                    number_y = TOP_MARGIN - 40
                    number_surface = text_create(str(j+1), 24, "white")
                    screen.blit(number_surface, (number_x, number_y))
            self.player_squares_left_top_corners.append(self.row)


        # Create board for second player
        for i in range(NUMBER_OF_RECTS):
            letter_x = LEFT_MARGIN - 30 + DISTANCE_BETWEEN_BOARDS + NUMBER_OF_RECTS * RECT_WIDTH
            letter_y = TOP_MARGIN + i * (RECT_HEIGHT) + RECT_HEIGHT // 2
            letter_surface = text_create(ALPHABET[i], 24, "white")
            screen.blit(letter_surface, (letter_x, letter_y))
            for j in range(NUMBER_OF_RECTS):
                rect_x = LEFT_MARGIN + j * RECT_WIDTH + j + DISTANCE_BETWEEN_BOARDS + NUMBER_OF_RECTS * RECT_WIDTH
                rect_y = TOP_MARGIN + i * RECT_HEIGHT + i
                rect = pygame.Rect(rect_x, rect_y , RECT_WIDTH, RECT_HEIGHT)
                pygame.draw.rect(screen, "white", rect)

                if (i == 0):
                    number_x = LEFT_MARGIN + j * (RECT_WIDTH + 1) + DISTANCE_BETWEEN_BOARDS + NUMBER_OF_RECTS * RECT_WIDTH + RECT_WIDTH // 2
                    number_y = TOP_MARGIN - 40
                    number_surface = text_create(str(j+1), 24, "white")
                    screen.blit(number_surface, (number_x, number_y))

        pygame.display.flip()
        
    # Create simple 2D array representing player board
    # 0 - empty cell
    # 1 - destoryer
    # 2 - submarine
    # 3 - cruiser
    # 4 - battleship
    # 5 - carrier
    def create_array_with_player_ships(self):
        self.player_board = [[0] * NUMBER_OF_RECTS for i in range(NUMBER_OF_RECTS)]
        self.player_board[0][1] = 1
        self.player_board[1][1] = 1
        self.player_board[4][1] = 2
        self.player_board[4][2] = 3
        self.player_board[5][5] = 4
        self.player_board[5][6] = 5
        
    def create_array_with_enemy_ships(self):
        self.enemy_board = [[0] * NUMBER_OF_RECTS for i in range(NUMBER_OF_RECTS)]
        self.enemy_board[5][3] = 1
        self.enemy_board[2][6] = 1
        self.enemy_board[6][2] = 2
        self.enemy_board[9][9] = 3
        self.enemy_board[3][1] = 4
        self.enemy_board[2][2] = 5

    # Function to color squares that contain ships with ships' coressponding color
    def draw_ships(self):
        for i in range(NUMBER_OF_RECTS):
            for j in range(NUMBER_OF_RECTS):
                # Check whether there is a ship on this square on player board
                if self.player_board[i][j] != 0:
                    # Determine color of the ship
                    color = SHIPS_COLORS[self.player_board[i][j] - 1]
                    rect_x = LEFT_MARGIN + j * RECT_WIDTH + j
                    rect_y = TOP_MARGIN + i * RECT_HEIGHT + i
                    rect = pygame.Rect(rect_x, rect_y , RECT_WIDTH, RECT_HEIGHT)
                    pygame.draw.rect(screen, color, rect)
                    self.board_squares.append(rect)

                if self.enemy_board[i][j] != 0:
                    color = SHIPS_COLORS[self.enemy_board[i][j] - 1]
                    rect_x = LEFT_MARGIN + j * RECT_WIDTH + j + DISTANCE_BETWEEN_BOARDS + RECT_WIDTH * NUMBER_OF_RECTS
                    rect_y = TOP_MARGIN + i * RECT_HEIGHT + i
                    rect = pygame.Rect(rect_x, rect_y , RECT_WIDTH, RECT_HEIGHT)
                    pygame.draw.rect(screen, color, rect)
                    self.board_squares.append(rect)

        pygame.display.flip()
        return
    
    def select_square(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, box in enumerate(self.board_squares):
                    if box.collidepoint(event.pos):
                        self.active_box = num
                        x,y = self.determine_square(self.board_squares[self.active_box].x, self.board_squares[self.active_box].y)
                        self.player_board[x][y] = "red"
                        self.draw_ships()
     
    def make_turn(self):

        self.whose_turn = 0 if self.whose_turn == 1 else 1 
        return

    def move_ship(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, box in enumerate(self.board_squares):
                    if box.collidepoint(event.pos):
                        self.active_box = num
                        square = self.determine_square(self.board_squares[self.active_box].x, self.board_squares[self.active_box].y)
                        if square is not -1:
                            x,y = square
                        self.picked_up_color = self.player_board[x][y]

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                square = self.determine_square(self.board_squares[self.active_box].x, self.board_squares[self.active_box].y)
                if square is not -1:
                    x,y = square                

                self.active_box = None

        if event.type == pygame.MOUSEMOTION:
            if self.active_box != None:
                self.board_squares[self.active_box].move_ip(event.rel)
                #print("Box " + str(self.active_box) + " was moved")
                #print(self.board_squares[self.active_box].x, self.board_squares[self.active_box].y)
            
