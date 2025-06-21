import pygame
import sys
from parameters import *
from classes import Game

SCREEN_WIDTH = NB_COL*CELL_SIZE
SCREEN_HEIGHT = NB_ROW*CELL_SIZE

def no_turn_back(current_dir, future_dir):
    """Checks if the current direction and future direction are opposites."""
    forbidden = {
        pygame.K_UP: pygame.K_DOWN,
        pygame.K_DOWN: pygame.K_UP,
        pygame.K_LEFT: pygame.K_RIGHT,
        pygame.K_RIGHT: pygame.K_LEFT
    }
    return forbidden[current_dir] != future_dir

def draw_gradient_background(top_color, bottom_color):
    """Draws a vertical gradient in the background (up to down)"""
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(top_color.r + ratio * (bottom_color.r - top_color.r))
        g = int(top_color.g + ratio * (bottom_color.g - top_color.g))
        b = int(top_color.b + ratio * (bottom_color.b - top_color.b))
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

def start_menu(score = None):
    
    while True:
        # Up to down gradient
        draw_gradient_background(pygame.Color("#a0d8f1"), pygame.Color("#003366"))

        # Game title
        title_font = pygame.font.SysFont(None, 72)
        title_text = title_font.render("SNAKE GAME", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title_text, title_rect)
        
        # Dynamic button color 
        mouse_pos = pygame.mouse.get_pos()
        if start_button.collidepoint(mouse_pos):
            button_color = pygame.Color("#dddddd")  
        else:
            button_color = WHITE  

        # Start button
        pygame.draw.rect(screen, button_color, start_button, border_radius=12)
        pygame.draw.rect(screen, BLACK, start_button, 2, border_radius=12)  # bordure
        start_text = font.render("START", True, BLACK)
        start_text_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, start_text_rect)
        
        # Score
        if score is not None:
            score_font = pygame.font.SysFont(None, 30)
            score_text = title_font.render(f"Your score: {score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 2*SCREEN_HEIGHT // 3))
            screen.blit(score_text, score_rect)
        
        # Update display
        pygame.display.update()

        # Quit game if closed and start game if start button pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return
                
def game_loop():
    """Main game loop."""
    timer = pygame.time.Clock()
    game = Game()   
    while True:
        for event in pygame.event.get():
            
            # Quit game if closed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Change snake direction if keyboard's arrows are used
            elif event.type == pygame.KEYDOWN:
                if no_turn_back(game.snake.direction, event.key):
                    game.snake.direction = event.key

        # draw background
        draw_gradient_background(pygame.Color("#a0d8f1"), pygame.Color("#003366"))
        
        # Update game by moving snake and handling game over and food eating
        game.update()
        if game.is_over:
            return game.score
        
        # draw snake and food
        game.draw(screen)
        pygame.display.update() 
        timer.tick(3) 
 
# Main program  
pygame.init()

# Screen
screen = pygame.display.set_mode((NB_COL*CELL_SIZE, NB_ROW*CELL_SIZE))
pygame.display.set_caption("Snake Game")
font = pygame.font.SysFont(None, FONT_SIZE)

# Start button
start_button = pygame.Rect(
    NB_COL*CELL_SIZE//2 - START_BUTTON_WIDTH//2, 
    NB_ROW*CELL_SIZE//2 -START_BUTTON_HEIGHT//2, 
    START_BUTTON_WIDTH , 
    START_BUTTON_HEIGHT
)

# Loop
score = None
while True:
    start_menu(score)
    score = game_loop()


    


