import pygame, math
from constants import *


class Pointer:
    def __init__(self, center):  
        self.center = center
        self.rad = 50 
        self.angle = 90         
        self.x = self.center.x + math.cos(math.radians(self.angle)) * self.rad
        self.y = self.center.y - math.sin(math.radians(self.angle)) * self.rad            
        # self.image = image  
        self.color = (255, 0, 0)         
        self.dx = 0
        self.dy = 0      
   
    def update(self, dt):
        self.angle += STARSHIP_ROTATING_SPEED * dt
        self.angle %= 360
        self.x = self.center.x + math.cos(math.radians(self.angle)) * self.rad
        self.y = self.center.y - math.sin(math.radians(self.angle)) * self.rad           

    def draw(self, screen):        
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)
        