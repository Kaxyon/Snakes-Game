import pygame
import random
import os

pygame.mixer.init()
pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)


# Creating Window
gameWindow = pygame.display.set_mode((720, 480))
pygame.display.set_caption('Snakes')
pygame.display.update()

# Background image
bg_img = pygame.image.load("bg.png")
bg_img = pygame.transform.scale(bg_img, (720, 480)).convert_alpha()

# font
font = pygame.font.SysFont(None, 55)
clock = pygame.time.Clock()

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# Welcome Screen
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233,220,229))
        text_screen("Welcome to Snakes", black, 200, 200)
        text_screen("Press Spacebar to Play", black, 170, 250)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('background.mp3')
                    pygame.mixer.music.play()
                    gameloop()
            

        pygame.display.update()
        clock.tick(60)

# Game Loop
def gameloop():

    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 10
    init_velocity = 4
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(0, 700)
    food_y = random.randint(0, 400)
    score = 0
    fps = 60
    snake_list = []
    snake_length = 1

    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")    
    with open("highscore.txt", "r") as f:
        highscore = f.read()

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            gameWindow.fill(white)
            text_screen("Game Over! Press Enter to continue", red, 30, 210)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()


        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score += 10

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x)<6 and abs(snake_y - food_y)<6:
                score += 10

                food_x = random.randint(0, 700)
                food_y = random.randint(0, 400)
                snake_length += 5
                if score > int(highscore):
                    highscore = score

            gameWindow.fill(white)
            gameWindow.blit(bg_img, (0, 0))
            text_screen(("Score:"+ str(score)) + "  Highscore: "+ str(highscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])



            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list)>snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('death.mp3')
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>720 or snake_y<0 or snake_y>480:
                game_over = True
                pygame.mixer.music.load('death.mp3')
                pygame.mixer.music.play()

            plot_snake(gameWindow, black, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)


    pygame.quit()
    quit()

welcome()
gameloop()