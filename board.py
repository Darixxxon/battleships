import pygame
import configparser

import client
import server

pygame.init()
screen = pygame.display.set_mode((1500, 900))
pygame.display.set_caption("Battle ships")
clock = pygame.time.Clock()
config = configparser.ConfigParser()
config.read("config.ini")

def surface_create(w, h, color=(255, 255, 255)):
    
    surface = pygame.Surface((w, h))
    surface.fill(color)
    return surface

def text_create(text, font_size=36, color=(0, 0, 0)):
    
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    return text_surface

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
      
if __name__ == "__main__":
    (type, host, port) = start_menu()
    if type == "Server":
        server.main_server(host, port)
    elif type == "Client":
        client.main_client(host, port)
    pygame.quit()
    quit()
    