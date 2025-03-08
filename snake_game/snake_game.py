import pygame
import time
import random

# Initialize pygame
pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Set display dimensions
display_width = 800
display_height = 600

# Set up the game display
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

# Set game clock
clock = pygame.time.Clock()

# Set snake block size and speed
snake_block = 20
snake_speed = 15

# Set fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def show_score(score):
    """Display current score on screen"""
    value = score_font.render("Score: " + str(score), True, black)
    display.blit(value, [0, 0])

def draw_snake(snake_block, snake_list):
    """Draw the snake on the screen"""
    for segment in snake_list:
        pygame.draw.rect(display, green, [segment[0], segment[1], snake_block, snake_block])

def message(msg, color):
    """Display message on screen"""
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [display_width / 6, display_height / 3])

def game_loop():
    """Main game loop"""
    game_over = False
    game_close = False

    # Initial snake position
    x1 = display_width / 2
    y1 = display_height / 2

    # Initial snake movement
    x1_change = 0
    y1_change = 0

    # Initialize snake
    snake_list = []
    snake_length = 1

    # Create initial food
    foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block

    while not game_over:

        while game_close:
            display.fill(white)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            show_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0

        # Check if snake hits boundary
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True

        # Update snake position
        x1 += x1_change
        y1 += y1_change

        # Fill display background
        display.fill(white)

        # Draw food
        pygame.draw.rect(display, red, [foodx, foody, snake_block, snake_block])

        # Update snake
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        # Remove extra snake segments if not eating food
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check if snake hits itself
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Draw snake and score
        draw_snake(snake_block, snake_list)
        show_score(snake_length - 1)

        # Update display
        pygame.display.update()

        # Check if snake eats food
        if x1 == foodx and y1 == foody:
            # Generate new food position
            foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
            # Increment snake length
            snake_length += 1

        # Set game speed
        clock.tick(snake_speed)

    # Quit pygame
    pygame.quit()
    quit()

if __name__ == "__main__":
    game_loop()
