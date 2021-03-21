import pygame
import math
from objects import Car, Wall, FinishLine

# Variables
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
WINDOW_SURFACE = pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE
red = (255,0,0)
blue = (0, 0, 255)
gray = (195, 195, 195)
points = 0
high_score = 0


# Initialization
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW_SURFACE)
pygame.display.set_caption('Super cool racing game')


# Car
car_image = pygame.image.load('car_image.png').convert_alpha()
car_image_size = car_image.get_size()
smaller_car_image = pygame.transform.scale(car_image, (int(car_image_size[0]/7), int(car_image_size[1]/7)))

car_spawn_x = WINDOW_WIDTH//2 + 120
car_spawn_y = WINDOW_HEIGHT//8
car1 = Car(smaller_car_image, car_spawn_x, car_spawn_y)

car_sprites = pygame.sprite.Group()
car_sprites.add(car1)


# Walls
WALLS = pygame.sprite.Group()

wall_1 = Wall(0,0, 1000, 20, blue, window)
wall_2 = Wall(0,580, 1000, 20 , blue, window)
wall_3 = Wall(0,0, 20, 600, blue, window)
wall_4 = Wall(980, 0, 20, 600, blue, window)

wall_5 = Wall(250, 150, 500, 10, blue, window)
wall_6 = Wall(250, 450, 500, 10, blue, window)
wall_7 = Wall(250, 150, 10, 300, blue, window)
wall_8 = Wall(750, 150, 10, 310, blue, window)

WALLS.add(wall_1)
WALLS.add(wall_2)
WALLS.add(wall_3)
WALLS.add(wall_4)

WALLS.add(wall_5)
WALLS.add(wall_6)
WALLS.add(wall_7)
WALLS.add(wall_8)



# Finish Line
FL = pygame.sprite.Group()
finish_line = FinishLine(WINDOW_WIDTH//2, 20, 50, 130, red, window)
FL.add(finish_line)


# Game
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WINDOW_WIDTH = event.w
            WINDOW_HEIGHT = event.h
            window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW_SURFACE)
    


    keys = pygame.key.get_pressed()
    if (keys[pygame.K_a]):
        if car1.speed != 0:
            car1.turn(-1.5)
    if (keys[pygame.K_d]):
        if car1.speed != 0:
            car1.turn(1.5)
    if (keys[pygame.K_w]):
        car1.accelerate(0.1)
    if (keys[pygame.K_s]):
        car1.brake(0.1)


    def display_text(variable, text, x, y):
        font = pygame.font.SysFont(None, 40)
        text = font.render(text + str(variable), 1, red)
        window.blit(text, (x,y))
    
    def check_highscore(current, highscore):
        if current > highscore:
            global high_score
            global points
            high_score = points

    # Fill Background
    window.fill(gray)

    # Display text
    display_text(points, 'Points: ', 430, (WINDOW_HEIGHT//2 - 25))
    display_text(high_score, 'High Score: ', 430, (WINDOW_HEIGHT//2 + 25))

    # Checks if the car has hit any wall
    col_wall = car1.check_wall_collision(car1, WALLS)
    if col_wall:
        points = 0
        check_highscore(points, high_score)
        display_text(points, 'Points: ', 430, (WINDOW_HEIGHT//2 - 25))
        display_text(high_score, 'High Score: ', 430, (WINDOW_HEIGHT//2 + 25))

    # Check if the car has hit the finish line and updates the score
    col_FL = car1.check_finishline_cross(finish_line)
    if col_FL:
        points += 1
        check_highscore(points, high_score)
        display_text(points, 'Points: ', 430, (WINDOW_HEIGHT//2 - 25))
        display_text(high_score, 'High Score: ', 430, (WINDOW_HEIGHT//2 + 25))
    elif col_FL == False:
        points = 0
        check_highscore(points, high_score)
        display_text(points, 'Points: ', 430, (WINDOW_HEIGHT//2 - 25))
        display_text(high_score, 'High Score: ', 430, (WINDOW_HEIGHT//2 + 25))

    # Update sprite groups
    car_sprites.update()
    WALLS.update()
    FL.update()
    
    # Draw sprite groups
    car_sprites.draw(window)
    WALLS.draw(window)
    FL.draw(window)


    pygame.display.flip()
    clock.tick_busy_loop(60)

pygame.quit()