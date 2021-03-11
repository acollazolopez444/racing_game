import pygame
import math
from objects import Car


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
WINDOW_SURFACE = pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE


pygame.mixer.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW_SURFACE)
pygame.display.set_caption('Driving Game Prototype')



road_image = pygame.image.load('track.png')
background = pygame.transform.smoothscale(road_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
car_image = pygame.image.load('car_image.png').convert_alpha()

car_size = car_image.get_size()
smaller_car = pygame.transform.scale(car_image, (int(car_size[0]/7), int(car_size[1]/7)))



car_spawn_x = WINDOW_WIDTH//5
car_spawn_y = WINDOW_HEIGHT//5
car1 = Car(smaller_car, car_spawn_x, car_spawn_y)
#car1 = Car(car_image, WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

car_sprites = pygame.sprite.Group()
car_sprites.add(car1)


clock = pygame.time.Clock()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.VIDEORESIZE:
            WINDOW_WIDTH = event.w
            WINDOW_HEIGHT = event.h
            window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW_SURFACE)
            background = pygame.transform.smoothscale(road_image, (WINDOW_WIDTH, WINDOW_HEIGHT))



    keys = pygame.key.get_pressed()
    if (keys[pygame.K_a]):
        if car1.speed != 0:
            car1.turn(-2)
    if (keys[pygame.K_d]):
        if car1.speed != 0:
            car1.turn(2)
    if (keys[pygame.K_w]):
        if car1.speed > -10 and car1.speed < 10:
            car1.accelerate(0.1)
            print(car1.speed)
    if (keys[pygame.K_s]):
        car1.brake(0.1)
        print(car1.speed)




    # Checkes rgb values for road background
    centerX, centerY = car1.rect.center
    pixel_color = background.get_at((centerX, centerY))
    #print(pixel_color)
    if pixel_color == (0, 0, 0, 255):
        car1.position = (car_spawn_x, car_spawn_y)
        car1.speed = 0
        #car1.heading = 0



    car_sprites.update()

    window.blit(background, (0,0))
    car_sprites.draw(window)
    pygame.display.flip()

    clock.tick_busy_loop(60)

pygame.quit()