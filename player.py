import pygame, random
from constants import *


class Player:
    def __init__(self, window_size, image):  
        self.max_x = window_size[0]
        self.max_y = window_size[1]       
        self.image = image       
        self.x = self.max_x // 2
        self.y = self.max_y // 2 
        self.dx = random.randint(-4 * PLAYER_FLYING_SPEED, 4 * PLAYER_FLYING_SPEED)
        self.dy = random.randint(-4 * PLAYER_FLYING_SPEED, 4 * PLAYER_FLYING_SPEED)        
        self.angle = 0
        self.dangle = random.randint(-4 * PLAYER_FLYING_SPEED, 4 * PLAYER_FLYING_SPEED)             
        self.isRunning = False
        
    def collide(self, mask, x, y):
        starship_mask = pygame.mask.from_surface(self.image[self.isRunning])
        offset = (int(self.x - x), int(self.y - y))
        is_collide = mask.overlap(starship_mask, offset)
        return is_collide

    def update(self):
        self.angle -= self.dangle
        self.x += self.dx
        self.y += self.dy

        if self.x > self.max_x + self.image[self.isRunning].get_width() // 2:
            self.x = -self.image[self.isRunning].get_width() // 2            
        if self.x < -self.image[self.isRunning].get_width() // 2:
            self.x = self.max_x + self.image[self.isRunning].get_width() // 2          
        if self.y > self.max_y + self.image[self.isRunning].get_height() // 2:
            self.y = -self.image[self.isRunning].get_height() // 2           
        if self.y < -self.image[self.isRunning].get_height() // 2:
            self.y = self.max_y + self.image[self.isRunning].get_height() // 2           
        
    def draw(self, screen): 
        img_copy = pygame.transform.rotate(self.image[self.isRunning], self.angle)       
        screen.blit(img_copy, (self.x - int(img_copy.get_width() / 2), self.y - int(img_copy.get_height() / 2)))   
       