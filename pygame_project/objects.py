import pygame
import math


class Car(pygame.sprite.Sprite):
    def  __init__(self, car_image, x, y, rotations = 360):
        pygame.sprite.Sprite.__init__(self)
        self.rot_img = []
        self.min_angle = (360/rotations)
        for i in range(rotations):
            rotated_image = pygame.transform.rotozoom(car_image, 360-90-(i*self.min_angle), 1)
            self.rot_img.append(rotated_image)
        self.min_angle = math.radians(self.min_angle)

        self.image = self.rot_img[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.heading = 0
        self.speed = 0
        self.velocity = pygame.math.Vector2(0,0)
        self.position = pygame.math.Vector2(x,y)
        self.x = x
        self.y = y

    def turn(self, angle_degrees):
        self.heading += math.radians(angle_degrees)
        image_index = int(self.heading/self.min_angle) % len(self.rot_img)

        if (self.image != self.rot_img[image_index]):
            x,y = self.rect.center
            self.image = self.rot_img[image_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)

    def accelerate(self, amount):
        if self.speed < 10:
            self.speed += amount

    def brake(self, amount):
        if self.speed > -10:
            self.speed -= amount

    def check_wall_collision(self, sprite, group):
        col = pygame.sprite.spritecollideany(sprite, group)
        if col:
            self.respawn()
            return True

    def check_finishline_cross(self, sprite):
        col = pygame.sprite.collide_rect(self, sprite)
        if col:
            # Checks if the car hit the left side which indicates the car made a complete lap
            if self.rect.collidepoint(sprite.rect.midleft) or self.rect.collidepoint((sprite.rect.left, 40)) or self.rect.collidepoint((sprite.rect.left, 100)):
                sprite.completed_lap = True
             # Checks if the car hit the right side of the finish line and if the car completed a lap
            if self.rect.collidepoint(sprite.rect.midright) or self.rect.collidepoint((sprite.rect.right, 40)) or self.rect.collidepoint((sprite.rect.right, 100)):
                if sprite.completed_lap == True and not sprite.get_point:
                    sprite.get_point = True
                    return True
                if sprite.completed_lap == False:
                    self.respawn()
                    return False
        else:
            sprite.completed_lap = False
            sprite.get_point = False
    
    def respawn(self):
        self.speed = 0
        self.position = (self.x, self.y)
        self.heading = 0
        self.image = self.rot_img[0]
        self.rect = self.image.get_rect()

    def update(self):
        self.velocity.from_polar((self.speed, math.degrees(self.heading)))
        self.position += self.velocity
        self.rect.center = (round(self.position[0]), round(self.position[1]))



class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, screen):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.screen = screen

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y


class FinishLine(Wall):
    def __init__(self, x, y, width, height, color, screen):
        super().__init__(x, y, width, height, color, screen)
        self.completed_lap = False
        self.get_point = False