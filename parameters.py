import pygame

# Sizes
NB_COL = 10
NB_ROW = 15
CELL_SIZE = 40
START_BUTTON_WIDTH = 200
START_BUTTON_HEIGHT = 60

# Colors
GAME_BACKGROUND_COLOR = (245, 245, 245)
FOOD_COLOR = (72, 212, 98)
SNAKE_COLOR = (83, 177, 253)

WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
GRAY = pygame.Color("gray")

# FONT
FONT_SIZE = 48


# Init snake position
INIT_SNAKE_BODY = [(4,4), (5,4), (6,4)]

# Game over message
GAME_OVER_MESSAGE = "Tu es mort avec un score de {score} ! C'est vraiment pathétique..."