import pygame
from constants import *


class Player:
    def __init__(self, window_size, image):  
        self.max_x = window_size[0]
        self.max_y = window_size[1]       
        self.image = image       
        self.x = self.max_x // 2
        self.y = self.max_y // 2 
        self.dx = 0
        self.dy = 0  
        self.angle = 0
        self.dangle = -1       
        self.impulse = 0
        self.isRunning = False
        
    def collide(self, mask, x, y):
        starship_mask = pygame.mask.from_surface(self.image[self.runnig])
        offset = (int(self.x - x), int(self.y - y))
        is_collide = mask.overlap(starship_mask, offset)
        return is_collide

    def update(self, dt):
        if self.impulse > 0:
            self.x += UFO_FLYING_SPEED * dt
            self.y += UFO_FLYING_SPEED * dt  

        self.angle += self.dangle
        if (self.x > self.max_x):
            self.x = 0
        if (self.y > self.max_y):
            self.y = 0
        if (self.x < 0):
            self.x = self.max_x
        if (self.y < 0):
            self.y = self.max_y      
        
    def draw(self, screen): 
        img_copy = pygame.transform.rotate(self.image[self.isRunning], self.angle)       
        screen.blit(img_copy, (self.x - int(img_copy.get_width() / 2), self.y - int(img_copy.get_height() / 2)))   
       