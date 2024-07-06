import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
ROOM_WIDTH = 600
ROOM_HEIGHT = 480
ROOM_X = 100
ROOM_Y = 60
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

furniture_dimensions = {
    'bed': (6, 4),
    'dresser': (3, 1.5),
    'tv_stand': (3, 1.5),
    'recliner': (3, 3),
    'et1': (1.5, 1.5),
    'et2': (1.5, 1.5)
}

furniture = {
    'bed': pygame.Rect(50, 500, 150, 100),
    'dresser': pygame.Rect(250, 500, 100, 50),
    'tv_stand': pygame.Rect(400, 500, 100, 50),
    'recliner': pygame.Rect(550, 500, 100, 100),
    'et1': pygame.Rect(50, 350, 50, 50),
    'et2': pygame.Rect(150, 350, 50, 50)
}

furniture_colors = {
    'bed': BLUE,
    'dresser': GREEN,
    'tv_stand': RED,
    'recliner': YELLOW,
    'et1': CYAN,
    'et2': MAGENTA
}

furniture_labels = {
    'bed': 'Bed',
    'dresser': 'Dresser',
    'tv_stand': 'TV Stand',
    'recliner': 'Recliner',
    'et1': 'ET1',
    'et2': 'ET2'
}

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Room Layout Designer')
font = pygame.font.SysFont(None, 24)

MENU = 'menu'
SETTINGS = 'settings'
LAYOUT = 'layout'
current_state = MENU

dragging = None
offset_x = 0
offset_y = 0

input_active = False
input_text = ''
furniture_count = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif current_state == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    current_state = SETTINGS
        elif current_state == SETTINGS:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        furniture_count = int(input_text)
                        input_text = ''
                        current_state = LAYOUT
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
        elif current_state == LAYOUT:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in furniture.items():
                    if rect.collidepoint(event.pos):
                        dragging = name
                        offset_x = rect.x - event.pos[0]
                        offset_y = rect.y - event.pos[1]
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = None
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    furniture[dragging].x = event.pos[0] + offset_x
                    furniture[dragging].y = event.pos[1] + offset_y

    screen.fill(WHITE)

    if current_state == MENU:
        start_button = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 - 25, 100, 50)
        pygame.draw.rect(screen, BLUE, start_button)
        start_text = font.render('Start', True, WHITE)
        screen.blit(start_text, (start_button.x + 25, start_button.y + 15))
    elif current_state == SETTINGS:
        settings_text = font.render('Enter number of furniture items:', True, BLACK)
        screen.blit(settings_text, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 50))
        input_box = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2, 100, 50)
        pygame.draw.rect(screen, BLUE, input_box, 2)
        input_surface = font.render(input_text, True, BLACK)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 15))
    elif current_state == LAYOUT:
        pygame.draw.rect(screen, BLUE, (ROOM_X, ROOM_Y, ROOM_WIDTH, ROOM_HEIGHT), 2)
        for name, rect in furniture.items():
            pygame.draw.rect(screen, furniture_colors[name], rect)
            label_text = font.render(furniture_labels[name], True, BLACK)
            label_rect = label_text.get_rect(center=rect.center)
            screen.blit(label_text, label_rect)
        if dragging:
            length, width = furniture_dimensions[dragging]
            dimension_text = f"{dragging.capitalize()}: {length}ft x {width}ft"
            text_surface = font.render(dimension_text, True, BLACK)
            screen.blit(text_surface, (10, 10))

    pygame.display.flip()
