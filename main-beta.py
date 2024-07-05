import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800  # Width of the game window in pixels
WINDOW_HEIGHT = 600  # Height of the game window in pixels
ROOM_WIDTH = 600  # Width of the room in pixels
ROOM_HEIGHT = 480  # Height of the room in pixels
ROOM_X = 100  # X-coordinate of the top-left corner of the room
ROOM_Y = 60  # Y-coordinate of the top-left corner of the room
WHITE = (255, 255, 255)  # Color code for white
BLUE = (0, 0, 255)  # Color code for blue
GREEN = (0, 255, 0)  # Color code for green
RED = (255, 0, 0)  # Color code for red
BLACK = (0, 0, 0)  # Color code for black
YELLOW = (255, 255, 0)  # Color code for yellow
CYAN = (0, 255, 255)  # Color code for cyan
MAGENTA = (255, 0, 255)  # Color code for magenta

# Placeholder dimensions (in feet)
furniture_dimensions = {
    'bed': (6, 4),  # Length x Width in feet
    'dresser': (3, 1.5),
    'tv_stand': (3, 1.5),
    'recliner': (3, 3),
    'end_table1': (1.5, 1.5),
    'end_table2': (1.5, 1.5)
}

# Furniture dictionary
# The 4 numbers in pygame.Rect represent (x, y, width, height) in pixels
furniture = {
    'bed': pygame.Rect(50, 500, 150, 100),  # x=50, y=500, width=150, height=100
    'dresser': pygame.Rect(250, 500, 100, 50),  # x=250, y=500, width=100, height=50
    'tv_stand': pygame.Rect(400, 500, 100, 50),  # x=400, y=500, width=100, height=50
    'recliner': pygame.Rect(550, 500, 100, 100),  # x=550, y=500, width=100, height=100
    'end_table1': pygame.Rect(50, 350, 50, 50),  # x=50, y=350, width=50, height=50
    'end_table2': pygame.Rect(150, 350, 50, 50)  # x=150, y=350, width=50, height=50
}

# Furniture colors
furniture_colors = {
    'bed': BLUE,
    'dresser': GREEN,
    'tv_stand': RED,
    'recliner': YELLOW,
    'end_table1': CYAN,
    'end_table2': MAGENTA
}

# Furniture labels
furniture_labels = {
    'bed': 'Bed',
    'dresser': 'Dresser',
    'tv_stand': 'TV Stand',
    'recliner': 'Recliner',
    'end_table1': 'E.T.1',
    'end_table2': 'E.T.2'
}

# Variables to track the currently dragged furniture and the mouse offset
dragging = None
offset_x = 0
offset_y = 0

# Font for displaying dimensions and labels
font = pygame.font.SysFont(None, 24)

# Setup display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Room Layout Designer')

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Handle quit event
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Handle mouse button down event
            for name, rect in furniture.items():
                if rect.collidepoint(event.pos):  # Check if a piece of furniture is clicked
                    dragging = name
                    offset_x = rect.x - event.pos[0]  # Calculate offset for smooth dragging
                    offset_y = rect.y - event.pos[1]
                    break
        elif event.type == pygame.MOUSEBUTTONUP:  # Handle mouse button up event
            dragging = None
        elif event.type == pygame.MOUSEMOTION:  # Handle mouse motion event
            if dragging:
                # Update the position of the dragged furniture
                furniture[dragging].x = event.pos[0] + offset_x
                furniture[dragging].y = event.pos[1] + offset_y

    screen.fill(WHITE)  # Clear the screen with white color

    # Draw the room boundary
    pygame.draw.rect(screen, BLUE, (ROOM_X, ROOM_Y, ROOM_WIDTH, ROOM_HEIGHT), 2)

    # Draw the furniture
    for name, rect in furniture.items():
        pygame.draw.rect(screen, furniture_colors[name], rect)
        # Render the furniture label in the center of the rectangle
        label_text = font.render(furniture_labels[name], True, BLACK)
        label_rect = label_text.get_rect(center=rect.center)
        screen.blit(label_text, label_rect)
    
    # Display dimensions of the selected furniture
    if dragging:
        length, width = furniture_dimensions[dragging]
        dimension_text = f"{dragging.capitalize()}: {length}ft x {width}ft"
        text_surface = font.render(dimension_text, True, BLACK)
        screen.blit(text_surface, (10, 10))  # Display text at the top-left corner

    pygame.display.flip()  # Update the display
