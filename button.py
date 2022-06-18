import pygame
from constants import *

class Button:
    def __init__(self, image):        
        self.image = image        
        self.x = 599
        self.y = 800

    def draw(self, screen, isPressed):
        screen.blit(self.image[isPressed], (self.x - int((self.image[isPressed].get_width() / 2)), self.y - int((self.image[isPressed].get_height() / 2))))
        