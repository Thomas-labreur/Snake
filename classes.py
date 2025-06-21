import pygame
import sys
from numpy.random import randint
from parameters import *

def convert( x, y):
    """Converts x and y in window coordinates"""
    return (CELL_SIZE * x, CELL_SIZE * y)

class Food():
    
    def __init__(self):
        self.x = randint(NB_COL)
        self.y = randint(NB_ROW)
        
    def draw(self, screen):
        """Draws food as a stylized red apple"""
        x, y = convert(self.x, self.y)
        center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
        radius = CELL_SIZE // 2 - CELL_SIZE//10

        # 🍎 Apple body
        pygame.draw.circle(screen, pygame.Color("red"), center, radius)
        
        # Apple stem
        stem_width = CELL_SIZE//10
        stem_height = CELL_SIZE//5
        stem_rect = pygame.Rect(center[0] - stem_width // 2, y + CELL_SIZE//10, stem_width, stem_height)
        pygame.draw.rect(screen, pygame.Color("saddlebrown"), stem_rect)

        # ✨ Reflection
        pygame.draw.circle(screen, pygame.Color("white"), (center[0] - CELL_SIZE//5, center[1] - CELL_SIZE//5), CELL_SIZE//10)

class Snake():
    
    def __init__(self):
        self.color = SNAKE_COLOR
        self.body = INIT_SNAKE_BODY
        self.size = CELL_SIZE
        self.direction = pygame.K_DOWN
        
    def draw(self, screen):
        """Draws snake's body on screen."""
        for i, (x, y) in enumerate(self.body):
            pos = convert(x, y)

            if i == len(self.body)-1:
                # 🟢 Snake head
                pygame.draw.rect(screen, pygame.Color("darkgreen"), (*pos, CELL_SIZE, CELL_SIZE), border_radius=CELL_SIZE//5)

                # 👀 Eyes
                eye_radius = CELL_SIZE//10
                eye_offset = CELL_SIZE//4
                pygame.draw.circle(screen, pygame.Color("white"), (pos[0] + eye_offset, pos[1] + eye_offset), eye_radius)
                pygame.draw.circle(screen, pygame.Color("white"), (pos[0] + 3*eye_offset, pos[1] + eye_offset), eye_radius)

            else:
                # 🟩 Snake body 
                color = pygame.Color("green") if i % 2 == 0 else pygame.Color("limegreen")
                pygame.draw.rect(screen, color, (*pos, CELL_SIZE, CELL_SIZE), border_radius=CELL_SIZE//5)

    
    def move(self):
        """Updates snake position."""
        
        # Move up
        if self.direction == pygame.K_UP:
            x, y = self.body[-1]
            self.body.append((x, y-1))

        # Move down
        elif self.direction == pygame.K_DOWN:
            x, y = self.body[-1]
            self.body.append((x, y+1))
         
        # Move left   
        elif self.direction == pygame.K_LEFT:
            x, y = self.body[-1]
            self.body.append((x-1, y))
        
        # Move right    
        elif self.direction == pygame.K_RIGHT:
            x, y = self.body[-1]
            self.body.append((x+1, y))
            
class Game():
    def __init__(self):
        self.score = 0
        self.is_over = False
        self.snake = Snake()
        self.generate_food()
        
    def draw(self, screen):
        """Draws snake and food."""
        self.snake.draw(screen)
        self.food.draw(screen)
        
    def update(self):
        """Updates snake position and handles food eating."""
        
        # Move snake position (by extending snake head)
        self.snake.move()
        
        # Checks for game over
        self.game_over()
        
        # If snake eats food, sdo not cut snake's tail and generate a new food
        is_snake_eating_food = (self.food.x, self.food.y) == self.snake.body[-1] 
        if is_snake_eating_food:   
            self.generate_food()
            self.score += 1
        else:
            self.snake.body = self.snake.body[1:]
            
    def generate_food(self):
        """Generates a new food."""
        self.food = Food()
        
        # Generate food again if food poped on the snake body
        is_food_on_snake = True
        while is_food_on_snake:
            count = 0
            for part in self.snake.body:
                count += (self.food.x, self.food.y) == part
            if count !=0:
                self.food = Food()
            else:
                is_food_on_snake = False
                
    def game_over(self):
        """If snake's head touches a window border or its own body, ends game."""
        snake_head = self.snake.body[-1]
        dead = False
        
        # Game is over if snake head touches its body
        for part in self.snake.body[:-1]:
            if part == snake_head:
                dead = True
                break
            
        # Or if snake head touches screen borders
        if dead or snake_head[0] not in range(NB_COL) or snake_head[1] not in range(NB_ROW):
            print(GAME_OVER_MESSAGE.format(score=self.score))
            self.is_over = True
            
        