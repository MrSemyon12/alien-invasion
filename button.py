import pygame
from constants import *

class Button:
    def __init__(self, image):        
        self.image = image        
        self.x = BUTTON_X
        self.y = BUTTON_Y

    def draw(self, screen, isPressed):
        screen.blit(self.image[isPressed], (self.x - int((self.image[isPressed].get_width() / 2)), self.y - int((self.image[isPressed].get_height() / 2))))
        