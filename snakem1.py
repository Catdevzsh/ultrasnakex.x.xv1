import pygame
import random
from array import array

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Define a function to generate beep sounds with varying frequencies
def generate_beep_sound(frequency=440, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * ((i // (sample_rate // frequency)) % 2)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound

# Sound definitions
move_sound = generate_beep_sound(440, 0.05)  # Beep sound for moving
eat_sound = generate_beep_sound(880, 0.1)    # Higher pitch beep for eating
game_over_sound = generate_beep_sound(220, 0.3)  # Lower pitch beep for game over

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Set window dimensions
display_width = 800
display_height = 600

# Create the display surface
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

# Set clock for controlling game speed
clock = pygame.time.Clock()

# Define snake properties
snake_block = 10
snake_speed = 15

# Define font for displaying score
font_style = pygame.font.SysFont(None, 35)

# Function to display the snake
def display_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(gameDisplay, green, [x[0], x[1], snake_block, snake_block])

# Function to display score
def display_score(score):
    value = font_style.render("Your Score: " + str(score), True, white)
    gameDisplay.blit(value, [0, 0])

# Main game loop
def gameLoop():
    game_over = False
    game_close = False

    # Initial snake position
    x1 = display_width / 2
    y1 = display_height / 2

    # Initial change in position
    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_length = 1

    # Generate initial food position
    foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            gameDisplay.fill(black)
            message = font_style.render("Game Over! Y-Play Again N-Exit", True, red)
            gameDisplay.blit(message, [display_width/6, display_height/3])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        gameLoop()
                    if event.key == pygame.K_n:
                        game_over = True
                        game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                move_sound.play()  # Play move sound on key press
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Update snake position
        x1 += x1_change
        y1 += y1_change

        # Boundary check for game over
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True
            game_over_sound.play()

        gameDisplay.fill(black)

        # Snake body mechanism
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check if snake hits itself
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        # Draw snake and food
        display_snake(snake_block, snake_list)
        pygame.draw.rect(gameDisplay, red, [foodx, foody, snake_block, snake_block])

        # Check if snake ate food
        if x1 == foodx and y1 == foody:
            eat_sound.play()  # Play eat sound
            foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            snake_length += 1

        # Display score
        display_score(snake_length - 1)

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
