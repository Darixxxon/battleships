import pygame
import configparser
from constants import (
    ATTACK_BUTTON_X, ATTACK_BUTTON_Y, CONFIRM_BUTTON_X, CONFIRM_BUTTON_Y,
    BACKGROUND_COLOR, TOTAL_SHIPS, NUMBER_OF_DESTROYERS, NUMBER_OF_SUBMARINES,
    NUMBER_OF_BATTLESHIPS, NUMBER_OF_CARRIERS, NUMBER_OF_CRUISERS, SHIPS,
    SCREEN_HEIGHT, SCREEN_WIDTH, RECT_WIDTH, RECT_HEIGHT, NUMBER_OF_RECTS,
    LEFT_MARGIN, TOP_MARGIN, DISTANCE_BETWEEN_BOARDS, ALPHABET
)

class Board:
    def __init__(self):
        """Initialize the game board with default values and settings."""
        # Game state variables
        self.game_stage = "placing"  # "placing", "battle", or "menu"
        self.whose_turn = 0  # 0 for player, 1 for enemy
        self.placing_ships = True
        self.all_ships_placed = False
        
        # UI elements
        self.active_box = None
        self.picked_up_color = None
        self.pickup_height = 0
        self.pickup_segment = 0
        self.last_valid_position = ()
        self.confirm_button = None
        self.attack_button = None
        
        # Board data structures
        self.player_grid = [[0 for _ in range(NUMBER_OF_RECTS)] for _ in range(NUMBER_OF_RECTS)]
        self.enemy_grid = [[0 for _ in range(NUMBER_OF_RECTS)] for _ in range(NUMBER_OF_RECTS)]
        self.attacked_tiles = [[0 for _ in range(NUMBER_OF_RECTS)] for _ in range(NUMBER_OF_RECTS)]
        self.enemy_attacked_tiles = [[0 for _ in range(NUMBER_OF_RECTS)] for _ in range(NUMBER_OF_RECTS)]
        self.selected_tiles = [[0 for _ in range(NUMBER_OF_RECTS)] for _ in range(NUMBER_OF_RECTS)]
        
        # Ship data
        self.ships_to_place = []
        self.placed_ships = []
        self.placed_ships_coordinates = []
        self.sunken_ships = []
        
        # Board coordinates
        self.player_squares = []
        self.enemy_squares = []
        self.enemy_squares_rects = []
        self.bounds = {'top': 0, 'bottom': 0, 'left': 0, 'right': 0}
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Battleship")
        self.clock = pygame.time.Clock()
        
        # Load configuration
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.background = self._create_surface(SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0))

    # --------------------------
    # Utility Methods
    # --------------------------
    
    def _create_surface(self, width, height, color=(255, 255, 255)):
        """Create a surface with given dimensions and color."""
        surface = pygame.Surface((width, height))
        surface.fill(color)
        return surface

    def _create_text(self, text, font_size=36, color=(0, 0, 0)):
        """Create a text surface with given parameters."""
        font = pygame.font.SysFont('Arial', font_size)
        return font.render(text, True, color)

    def _create_rect(self, x, y, width, height, color=(255, 255, 255)):
        """Create and draw a rectangle on the screen."""
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, rect)
        return rect

    # --------------------------
    # Game State Management
    # --------------------------
    
    def get_game_stage(self):
        """Return the current game stage."""
        return self.game_stage

    def switch_turn(self):
        """Switch turns between player and enemy."""
        self.whose_turn = 0 if self.whose_turn == 1 else 1
        return self.whose_turn

    # --------------------------
    # Menu Screens
    # --------------------------
    
    def start_menu(self):
        """Simplified start menu for choosing server/client mode with click feedback."""
        title_surface = self._create_text("Welcome to Battleships", 48, "white")
        server_button = pygame.Rect(300, 300, 300, 100)
        client_button = pygame.Rect(800, 300, 300, 100)

        clicked_button = None  # track which button is clicked
        click_time = 0

        while True:
            self.screen.fill((0, 0, 0))

            # Draw title
            self.screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 100))

            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Determine button colors
            server_color = (180, 180, 180) if server_button.collidepoint(mouse_pos) else "white"
            client_color = (180, 180, 180) if client_button.collidepoint(mouse_pos) else "white"

            # Visual feedback if clicked
            if clicked_button and pygame.time.get_ticks() - click_time < 150:
                if clicked_button == "Server":
                    server_color = (100, 255, 100)
                elif clicked_button == "Client":
                    client_color = (100, 255, 100)

            # Draw buttons
            pygame.draw.rect(self.screen, server_color, server_button)
            pygame.draw.rect(self.screen, client_color, client_button)

            self.screen.blit(self._create_text("Server", 36, "black"), (server_button.x + 90, server_button.y + 30))
            self.screen.blit(self._create_text("Client", 36, "black"), (client_button.x + 90, client_button.y + 30))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if server_button.collidepoint(event.pos):
                        clicked_button = "Server"
                        click_time = pygame.time.get_ticks()
                    elif client_button.collidepoint(event.pos):
                        clicked_button = "Client"
                        click_time = pygame.time.get_ticks()

            # After brief delay, return selection
            if clicked_button and pygame.time.get_ticks() - click_time >= 150:
                if clicked_button == "Server":
                    host = self.config.get('SERVER', 'HOST_IP')
                    port = self.config.get('SERVER', 'HOST_PORT')
                    return ("Server", host, port)
                elif clicked_button == "Client":
                    host = self.config.get('CLIENT', 'HOST_IP')
                    port = self.config.get('CLIENT', 'HOST_PORT')
                    return ("Client", host, port)



    def _draw_menu_section(self, title, host_text, port_text, host_surface, port_surface, choose_surface, x_pos):
        """Helper method to draw a menu section (server or client)."""
        # Title
        self.screen.blit(self._create_surface(200, 75), (x_pos - 100, 225))
        self.screen.blit(self._create_text(title), (x_pos - 50, 225))
        
        # Host input
        self.screen.blit(host_surface, (x_pos - 150, 325))
        self.screen.blit(self._create_text("HOST:"), (x_pos - 250, 325))
        self.screen.blit(self._create_text(host_text), (x_pos - 150, 325))
        
        # Port input
        self.screen.blit(port_surface, (x_pos - 150, 425))
        self.screen.blit(self._create_text("PORT:"), (x_pos - 250, 425))
        self.screen.blit(self._create_text(port_text), (x_pos - 150, 425))
        
        # Choose button
        self.screen.blit(choose_surface, (x_pos - 100, 525))
        self.screen.blit(self._create_text("Choose"), (x_pos - 75, 525))

    # --------------------------
    # Ship Placement Phase
    # --------------------------
    
    def choose_layout(self):
        """Handle the ship placement phase of the game."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return
                
                if self.game_stage == "placing":
                    self._handle_placement_phase(event)
                else:
                    return
                
                pygame.display.flip()

    def _handle_placement_phase(self, event):
        """Handle events during the ship placement phase."""
        self._create_positioning_board()
        self._create_ships_to_place()
        self._draw_ships_to_place()
        self._place_ships(event)
        self._show_confirm_button()
        self._confirm_button_pressed(event)

    def _create_positioning_board(self):
        """Create the board for ship placement."""
        self.bounds = {'top': 0, 'bottom': 0, 'left': 0, 'right': 0}
        self.placing_squares = []
        
        board_center_x = SCREEN_WIDTH // 2 - RECT_WIDTH * NUMBER_OF_RECTS // 2
        
        # Draw letters (vertical coordinates)
        for i in range(NUMBER_OF_RECTS):
            letter_x = board_center_x - RECT_WIDTH
            letter_y = TOP_MARGIN // 2 + i * (RECT_HEIGHT) + RECT_HEIGHT // 2
            self.screen.blit(self._create_text(ALPHABET[i], 24, "white"), (letter_x, letter_y))

            row = []
            for j in range(NUMBER_OF_RECTS):
                rect_x = board_center_x + j * (RECT_WIDTH + 1)
                rect_y = TOP_MARGIN // 2 + i * (RECT_HEIGHT + 1)
                
                # Draw grid square
                rect = pygame.Rect(rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, width=1)
                
                row.append([(i, j), (rect_x, rect_y)])
                
                # Draw numbers (horizontal coordinates) on first row
                if i == 0:
                    number_x = rect_x + RECT_WIDTH // 2
                    number_y = TOP_MARGIN // 2 - 40
                    self.screen.blit(self._create_text(str(j+1), 24, "white"), (number_x, number_y))

                # Set bounds
                if i == 0 and j == 0:
                    self.bounds.update({
                        'top': rect_y,
                        'left': rect_x
                    })
                if i == NUMBER_OF_RECTS - 1 and j == NUMBER_OF_RECTS - 1:
                    self.bounds.update({
                        'bottom': rect_y + RECT_HEIGHT,
                        'right': rect_x + RECT_WIDTH
                    })

            self.placing_squares.append(row)

    # def _create_ships_to_place(self):
    #     """Create all ships that need to be placed on the board."""
    #     if not self.ships_to_place:
    #         ship_types = [
    #             ('destroyer', NUMBER_OF_DESTROYERS),
    #             ('submarine', NUMBER_OF_SUBMARINES),
    #             ('cruiser', NUMBER_OF_CRUISERS),
    #             ('battleship', NUMBER_OF_BATTLESHIPS),
    #             ('carrier', NUMBER_OF_CARRIERS)
    #         ]
            
    #         for ship_type, count in ship_types:
    #             for i in range(count):
    #                 x = SCREEN_WIDTH // 2 - RECT_WIDTH * NUMBER_OF_RECTS // 2 + len(self.ships_to_place) * (RECT_WIDTH + 10)
    #                 y = TOP_MARGIN + RECT_HEIGHT * NUMBER_OF_RECTS
    #                 self._create_ship_to_place(ship_type, x, y)

    def _create_ship_to_place(self, ship_type, x, y):
        """Create a specific type of ship to be placed."""
        params = SHIPS[ship_type]
        width = params[2] if params[2] > params[1] else params[1]
        height = params[1] if params[2] > params[1] else params[2]
        
        rect = pygame.Rect(x, y, width, height)
        self.ships_to_place.append([rect, params[0], False])  # [rect, color, is_placed]


    def _create_ships_to_place(self):
        if not self.ships_to_place:
            ship_types = [
                ('destroyer', NUMBER_OF_DESTROYERS),
                ('submarine', NUMBER_OF_SUBMARINES),
                ('cruiser', NUMBER_OF_CRUISERS),
                ('battleship', NUMBER_OF_BATTLESHIPS),
                ('carrier', NUMBER_OF_CARRIERS)
            ]
            
            x = SCREEN_WIDTH // 4 - RECT_WIDTH * NUMBER_OF_RECTS // 2
            y = TOP_MARGIN + RECT_HEIGHT * NUMBER_OF_RECTS
            gap = 10  # space between ships

            for ship_type, count in ship_types:
                for _ in range(count):
                    params = SHIPS[ship_type]
                    width = params[2] if params[2] > params[1] else params[1]
                    height = params[1] if params[2] > params[1] else params[2]
                    
                    self._create_ship_to_place(ship_type, x, y)  # <-- correct method name here
                    x += width + gap


    def _draw_ships_to_place(self):
        """Draw all ships that are available for placement."""
        for ship in self.ships_to_place:
            if not ship[2]:  # Only draw if not placed
                pygame.draw.rect(self.screen, ship[1], ship[0])

    def _place_ships(self, event):
        """Handle ship placement logic."""
        if event.type == pygame.KEYDOWN and self.active_box is not None and event.key == pygame.K_q:
            self._rotate_ship()
            return
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_ship_pickup(event)
            
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.active_box is not None:
            self._handle_ship_drop()
            
        if event.type == pygame.MOUSEMOTION and self.active_box is not None:
            self._handle_ship_drag(event)

    # def _rotate_ship(self):
    #     """Rotate the currently active ship."""
    #     ship_rect = self.ships_to_place[self.active_box][0]
    #     ship_rect.width, ship_rect.height = ship_rect.height, ship_rect.width
    #     ship_rect.x -= (ship_rect.height - ship_rect.width) // 2
    #     ship_rect.y -= (ship_rect.width - ship_rect.height) // 2
    #     self._redraw_all()

    def _rotate_ship(self):
        ship_rect = self.ships_to_place[self.active_box][0]
        
        # Store old width and height
        old_width, old_height = ship_rect.width, ship_rect.height
        
        # Swap width and height
        ship_rect.width, ship_rect.height = old_height, old_width
        
        # Adjust position to keep mouse pointer at the same relative position
        # The offset from top-left to mouse should be swapped accordingly
        
        new_x = ship_rect.x + self.drag_offset_x - self.drag_offset_y
        new_y = ship_rect.y + self.drag_offset_y - self.drag_offset_x
        
        # This might need fine-tuning depending on your orientation logic:
        # A simpler way is to calculate the mouse pos and keep it constant
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Calculate new top-left so mouse stays at same relative position in rotated rect
        new_x = mouse_x - self.drag_offset_y
        new_y = mouse_y - self.drag_offset_x
        
        ship_rect.topleft = (new_x, new_y)
        
        self._redraw_all()


    # def _handle_ship_pickup(self, event):
    #     """Handle picking up a ship for placement."""
    #     for num, ship in enumerate(self.ships_to_place):
    #         if not ship[2] and ship[0].collidepoint(event.pos):
    #             self.active_box = num
    #             self.picked_up_color = ship[1]
    #             self.last_valid_position = ship[0].topleft
                
    #             # Calculate which segment was clicked
    #             ship_rect = ship[0]
    #             click_y = event.pos[1] - ship_rect.y
    #             self.pickup_segment = min(int(click_y / RECT_HEIGHT), ship_rect.height - 1)
    #             break
    def _handle_ship_pickup(self, event):
        for num, ship in enumerate(self.ships_to_place):
            if not ship[2] and ship[0].collidepoint(event.pos):
                self.active_box = num
                self.picked_up_color = ship[1]
                self.last_valid_position = ship[0].topleft
                
                # Calculate offset between mouse and ship top-left
                ship_rect = ship[0]
                self.drag_offset_x = event.pos[0] - ship_rect.x
                self.drag_offset_y = event.pos[1] - ship_rect.y
                
                # Calculate which segment was clicked (keep if needed)
                click_y = event.pos[1] - ship_rect.y
                self.pickup_segment = min(int(click_y / RECT_HEIGHT), ship_rect.height - 1)
                break


    def _handle_ship_drop(self):
        """Handle dropping a ship after placement attempt."""
        ship = self.ships_to_place[self.active_box]
        mouse_pos = pygame.mouse.get_pos()
        square = self._determine_square(mouse_pos[0], mouse_pos[1])
        
        if square != -1 and self._is_valid_placement(ship, square):
            self._finalize_ship_placement(ship, square)
        else:
            ship[0].topleft = self.last_valid_position
            
        self.active_box = None
        self._redraw_all()

    def _is_valid_placement(self, ship, square):
        """Check if a ship can be placed at the given position."""
        grid_y, grid_x = square
        ship_rect = ship[0]
        is_vertical = ship_rect.height > ship_rect.width
        
        if is_vertical:
            ship_length = int(ship_rect.height // RECT_HEIGHT)
            start_y = grid_y - self.pickup_segment
            return all(
                0 <= start_y + i < NUMBER_OF_RECTS and 
                self.player_grid[start_y + i][grid_x] == 0
                for i in range(ship_length))
        else:
            ship_length = int(ship_rect.width // RECT_WIDTH)
            start_x = grid_x - self.pickup_segment
            return all(
                0 <= start_x + i < NUMBER_OF_RECTS and 
                self.player_grid[grid_y][start_x + i] == 0
                for i in range(ship_length))

    def _finalize_ship_placement(self, ship, square):
        """Finalize the placement of a ship on the board."""
        grid_y, grid_x = square
        ship_rect = ship[0]
        is_vertical = ship_rect.height > ship_rect.width
        
        if is_vertical:
            ship_length = int(ship_rect.height // RECT_HEIGHT)
            start_y = grid_y - self.pickup_segment
            new_x = self.placing_squares[0][grid_x][1][0]
            new_y = self.placing_squares[start_y][0][1][1]
        else:
            ship_length = int(ship_rect.width // RECT_WIDTH)
            start_x = grid_x - self.pickup_segment
            new_x = self.placing_squares[0][start_x][1][0]
            new_y = self.placing_squares[grid_y][0][1][1]
        
        ship_rect.topleft = (new_x, new_y)
        self.last_valid_position = (new_x, new_y)
        ship[2] = True  # Mark as placed
        self.placed_ships.append(ship)
        self._update_occupancy_grid(ship, grid_y, grid_x, is_vertical)
        self._check_all_ships_placed()

    def _update_occupancy_grid(self, ship, grid_y, grid_x, is_vertical):
        """Update the grid to mark occupied squares."""
        ship_id = self._get_ship_id(ship[1])
        ship_length = int(ship[0].height // RECT_HEIGHT) if is_vertical else int(ship[0].width // RECT_WIDTH)
        
        for i in range(-1, ship_length + 1):
            for j in range(-1, 2):  # -1, 0, 1
                y = grid_y + (i if is_vertical else 0) - (self.pickup_segment if is_vertical else 0)
                x = grid_x + (j if is_vertical else i) - (0 if is_vertical else self.pickup_segment)
                
                if 0 <= y < NUMBER_OF_RECTS and 0 <= x < NUMBER_OF_RECTS:
                    if 0 <= i < ship_length and j == 0:
                        self.player_grid[y][x] = ship_id
                    elif self.player_grid[y][x] == 0:
                        self.player_grid[y][x] = 9  # Mark as buffer zone

    def _check_all_ships_placed(self):
        """Check if all ships have been placed."""
        self.all_ships_placed = len(self.placed_ships) == TOTAL_SHIPS

    def _handle_ship_drag(self, event):
        """Handle dragging a ship around the board."""
        self._redraw_all()
        self.ships_to_place[self.active_box][0].move_ip(event.rel)
        pygame.draw.rect(self.screen, self.picked_up_color, self.ships_to_place[self.active_box][0])
        pygame.display.flip()

    def _redraw_all(self):
        """Redraw all game elements."""
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw unplaced ships
        for i, ship in enumerate(self.ships_to_place):
            if i != self.active_box and not ship[2]:
                pygame.draw.rect(self.screen, ship[1], ship[0])

        # Draw board
        self._create_positioning_board()

        # Draw placed ships
        for ship in self.placed_ships:
            pygame.draw.rect(self.screen, ship[1], ship[0])

        # Draw active ship on top
        if self.active_box is not None:
            active_ship = self.ships_to_place[self.active_box]
            pygame.draw.rect(self.screen, active_ship[1], active_ship[0])

        pygame.display.flip()

    def _show_confirm_button(self):
        """Show the confirm button centered with subtitle and hover effect."""
        if not self.all_ships_placed:
            return  # Don't show if not all ships placed

        # Button dimensions
        button_width = RECT_WIDTH * 3
        button_height = int(RECT_HEIGHT * 1.5)
        screen_width = self.screen.get_width()

        # Center button horizontally and place vertically near bottom quarter
        button_x = (screen_width - button_width) // 2
        button_y = int(self.screen.get_height() * 0.75)

        self.confirm_button = pygame.Rect(button_x, button_y, button_width, button_height)

        # Get mouse position for hover effect
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.confirm_button.collidepoint(mouse_pos)

        # Draw button with hover color
        button_color = (180, 180, 180) if is_hovered else (128, 128, 128)
        pygame.draw.rect(self.screen, button_color, self.confirm_button, border_radius=8)

        # Draw button text centered inside the button
        confirm_text = self._create_text("CONFIRM", 28, "black")
        text_rect = confirm_text.get_rect(center=self.confirm_button.center)
        self.screen.blit(confirm_text, text_rect)

        # Subtitle above the button, centered
        subtitle_text = self._create_text("All ships placed! Ready to start?", 20, "white")
        subtitle_rect = subtitle_text.get_rect(center=(screen_width // 2, button_y - 30))
        self.screen.blit(subtitle_text, subtitle_rect)

        # Info message below the button
        info_text = self._create_text("Click Confirm to start the battle!", 18, "lightgray")
        info_rect = info_text.get_rect(center=(screen_width // 2, button_y + button_height + 20))
        self.screen.blit(info_text, info_rect)

        pygame.display.flip()


    def _confirm_button_pressed(self, event):
        """Handle confirm button press to start the battle."""
        if self.confirm_button and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.confirm_button.collidepoint(event.pos):
                # Prepare placed ships coordinates for battle
                self.placed_ships_coordinates.clear()
                for ship in self.placed_ships:
                    coords_list = []
                    ship_rect = ship[0]
                    is_vertical = ship_rect.height > ship_rect.width
                    length = int(ship_rect.height // RECT_HEIGHT) if is_vertical else int(ship_rect.width // RECT_WIDTH)
                    grid_y, grid_x = self._determine_square(ship[0].x, ship[0].y)
                    for i in range(length):
                        y = grid_y + i if is_vertical else grid_y
                        x = grid_x if is_vertical else grid_x + i
                        coords_list.append((y, x))
                    self.placed_ships_coordinates.append((ship, coords_list))

                self.game_stage = "battle"
                self.placing_ships = False
                self.screen.fill(BACKGROUND_COLOR)
                pygame.display.flip()
                return True
        return False


    def _get_ship_id(self, color):
        """Get the ID of a ship based on its color."""
        for ship_params in SHIPS.values():
            if ship_params[0] == color:
                return ship_params[3]
        return -1

    # --------------------------
    # Battle Phase
    # --------------------------
    
    def battle(self):
        """Handle the battle phase of the game."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return None
                
                if self.game_stage == "battle":
                    self._draw_battle_screen()
                    result = self._handle_battle_events(event)
                    if result and result[0]:  # If attack was made
                        return (result[1], result[2])  # Return coordinates
                
                pygame.display.flip()

    def _draw_battle_screen(self):
        """Draw the battle screen with both player and enemy boards."""
        self.screen.fill(BACKGROUND_COLOR)
        self._create_playing_board()
        self._draw_player_ships()
        self._draw_enemy_hits()

    def _create_playing_board(self):
        """Create the playing boards for both players."""
        self.player_squares = []
        self.enemy_squares = []
        self.enemy_squares_rects = []
        
        # Player board
        self._draw_single_board(LEFT_MARGIN, "Player Board", 0)
        
        # Enemy board
        self._draw_single_board(
            LEFT_MARGIN + DISTANCE_BETWEEN_BOARDS + NUMBER_OF_RECTS * RECT_WIDTH, 
            "Enemy Board", 
            1
        )
        
        # Turn indicator
        turn_text = "Your turn" if self.whose_turn == 0 else "Enemy's turn"
        self.screen.blit(
            self._create_text(turn_text, 36, "white"),
            (SCREEN_WIDTH // 2 - 100, TOP_MARGIN - 75)
        )

    def _draw_single_board(self, x_offset, title, board_type):
        """Draw a single game board (player or enemy)."""
        # Draw title
        title_surface = self._create_text(title, 24, "white")
        self.screen.blit(title_surface, (x_offset + NUMBER_OF_RECTS * RECT_WIDTH // 2 - 50, TOP_MARGIN - 70))
        
        squares = []
        
        for i in range(NUMBER_OF_RECTS):
            # Draw vertical coordinate letters
            letter_x = x_offset - 30
            letter_y = TOP_MARGIN + i * (RECT_HEIGHT) + RECT_HEIGHT // 2
            self.screen.blit(self._create_text(ALPHABET[i], 24, "white"), (letter_x, letter_y))

            row = []
            for j in range(NUMBER_OF_RECTS):
                rect_x = x_offset + j * (RECT_WIDTH + 1)
                rect_y = TOP_MARGIN + i * (RECT_HEIGHT + 1)
                rect = pygame.Rect(rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT)
                
                # Draw the square with appropriate color
                if board_type == 0:  # Player board
                    pygame.draw.rect(self.screen, "white", rect)
                else:  # Enemy board
                    self._draw_enemy_square(rect, i, j)
                    if len(self.enemy_squares_rects) < NUMBER_OF_RECTS ** 2:
                        self.enemy_squares_rects.append(rect)
                
                row.append([(i, j), (rect_x, rect_y)])
                
                # Draw horizontal coordinate numbers
                if i == 0:
                    number_x = rect_x + RECT_WIDTH // 2
                    number_y = TOP_MARGIN - 40
                    self.screen.blit(self._create_text(str(j+1), 24, "white"), (number_x, number_y))

            if board_type == 0:
                self.player_squares.append(row)
            else:
                self.enemy_squares.append(row)

    def _check_if_enemy_sunk(self):
        """Check if all enemy ship tiles have been hit."""
        for i in range(NUMBER_OF_RECTS):
            for j in range(NUMBER_OF_RECTS):
                if self.enemy_grid[i][j] > 0 and self.attacked_tiles[i][j] != 2:
                    return True
        return False


    def _draw_enemy_square(self, rect, i, j):
        """Draw an enemy square with appropriate markings."""
        # Base square
        pygame.draw.rect(self.screen, "white", rect)
        
        # Selected tile highlight
        if self.selected_tiles[i][j]:
            pygame.draw.rect(self.screen, "red", rect, 2)
        
        # Attack results
        if self.attacked_tiles[i][j] == 1:  # Miss
            self._draw_miss_marker(rect)
        elif self.attacked_tiles[i][j] == 2:  
            self._draw_hit_marker(rect)
            if self._check_if_enemy_sunk():
                self._display_game_over(winner="You")


    def _draw_miss_marker(self, rect):
        """Draw a miss marker (X) on the square."""
        start_pos1 = (rect.x + 5, rect.y + 5)
        end_pos1 = (rect.x + rect.width - 5, rect.y + rect.height - 5)
        start_pos2 = (rect.x + rect.width - 5, rect.y + 5)
        end_pos2 = (rect.x + 5, rect.y + rect.height - 5)
        pygame.draw.line(self.screen, "red", start_pos1, end_pos1, 2)
        pygame.draw.line(self.screen, "red", start_pos2, end_pos2, 2)

    def _draw_hit_marker(self, rect):
        """Draw a hit marker (circle) on the square."""
        center = (rect.x + rect.width // 2, rect.y + rect.height // 2)
        radius = rect.width // 2 - 5
        pygame.draw.circle(self.screen, "red", center, radius, 2)

    def _draw_player_ships(self):
        """Draw the player's ships on their board."""
        for ship_data in self.placed_ships_coordinates:
            ship, coords_list = ship_data
            for grid_y, grid_x in coords_list:
                position = self._get_square_coordinates(grid_y, grid_x)
                if position:
                    new_rect = pygame.Rect(
                        position[0], position[1],
                        RECT_WIDTH, RECT_HEIGHT
                    )
                    pygame.draw.rect(self.screen, ship[1], new_rect)


    def _get_square_coordinates(self, x, y):
        """Get screen coordinates for a grid square."""
        if 0 <= x < NUMBER_OF_RECTS and 0 <= y < NUMBER_OF_RECTS:
            return self.player_squares[x][y][1]
        return None

    def _draw_enemy_hits(self):
        """Draw enemy attacks on the player's board."""
        for i in range(NUMBER_OF_RECTS):
            for j in range(NUMBER_OF_RECTS):
                if self.enemy_attacked_tiles[i][j] == 1:  # Miss
                    rect = pygame.Rect(*self._get_square_coordinates(i, j), RECT_WIDTH, RECT_HEIGHT)
                    self._draw_miss_marker(rect)
                elif self.enemy_attacked_tiles[i][j] == 2:  # Hit
                    rect = pygame.Rect(*self._get_square_coordinates(i, j), RECT_WIDTH, RECT_HEIGHT)
                    self._draw_hit_marker(rect)

    def _handle_battle_events(self, event):
        """Handle events during the battle phase."""
        self._select_square(event)
        self._show_attack_button()
        return self._attack_button_pressed(event)

    def _select_square(self, event):
        """Handle selecting a square on the enemy board."""
        if self.whose_turn == 0 and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.enemy_squares_rects):
                if rect.collidepoint(event.pos):
                    grid_y = i // NUMBER_OF_RECTS
                    grid_x = i % NUMBER_OF_RECTS
                    
                    # Reset selection and select the new square
                    self.selected_tiles = [[0 for _ in range(NUMBER_OF_RECTS)] for _ in range(NUMBER_OF_RECTS)]
                    self.selected_tiles[grid_y][grid_x] = 1
                    self.chosen_tile = (grid_y, grid_x)
                    break

    def _show_attack_button(self):
        """Show the attack button during the player's turn."""
        if self.whose_turn == 0:
            self.attack_button = pygame.Rect(
                ATTACK_BUTTON_X, ATTACK_BUTTON_Y,
                RECT_WIDTH * 3, RECT_HEIGHT * 1.5
            )
            pygame.draw.rect(self.screen, "gray", self.attack_button)
            self.screen.blit(
                self._create_text("ATTACK", 24, "black"),
                (ATTACK_BUTTON_X + 10, ATTACK_BUTTON_Y + 10)
            )

    def _attack_button_pressed(self, event):
        """Handle attack button press."""
        if self.whose_turn == 0 and self.attack_button and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.attack_button.collidepoint(event.pos):
                self.screen.fill(BACKGROUND_COLOR)
                
                # Find the selected square
                for i in range(NUMBER_OF_RECTS):
                    for j in range(NUMBER_OF_RECTS):
                        if self.selected_tiles[i][j] == 1:
                            self.selected_tiles = [[0 for _ in range(NUMBER_OF_RECTS)] for _ in range(NUMBER_OF_RECTS)]
                            return (True, i, j)  # Attack made at (i, j)
        return (False,)
    
    def _check_if_all_ships_sunk(self):
        """Check if all player's ship tiles have been hit."""
        for _, ship_coords in self.placed_ships_coordinates:
            for y, x in ship_coords:
                if self.enemy_attacked_tiles[y][x] != 2:
                    return False
        return True
    
    def _display_game_over(self, winner="Unknown"):
        """Display game over screen and wait for user to quit."""
        self.screen.fill((0, 0, 0))
        message = f"{winner} wins!"
        text = self._create_text(message, 64, (255, 0, 0))
        self.screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 32))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()



    def receiving_attack(self, attack):
        """Process an attack from the enemy and check for game over."""
        x, y = attack
        hit = False

        for ship_data in self.placed_ships_coordinates:
            ship_coords = ship_data[1]
            if (x, y) in ship_coords:
                self.enemy_attacked_tiles[x][y] = 2  # Hit
                hit = True
                break

        if not hit:
            self.enemy_attacked_tiles[x][y] = 1  # Miss

        if self._check_if_all_ships_sunk():
            self._display_game_over(winner="Enemy")
        
        return hit


    def _determine_square(self, x, y):
        """Determine which grid square contains the given coordinates."""
        if not (self.bounds['left'] <= x < self.bounds['right'] and 
                self.bounds['top'] <= y < self.bounds['bottom']):
            return -1
            
        grid_y = int((y - self.bounds['top']) // (RECT_HEIGHT + 1))
        grid_x = int((x - self.bounds['left']) // (RECT_WIDTH + 1))
        
        if 0 <= grid_y < NUMBER_OF_RECTS and 0 <= grid_x < NUMBER_OF_RECTS:
            return (grid_y, grid_x)
        return -1
    
    def make_turn(self):
        self.whose_turn = 0 if self.whose_turn == 1 else 1 
        return