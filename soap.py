# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 15:32:44 2020

@author: User
"""


from config import *
import pygame, random
from pygame.locals import *

#soap class created
class Soap(pygame.sprite.Sprite):
    
    #The soap is initialized. 
    def __init__(self, image, sound):
        super().__init__()
        self.rect = image.get_rect()
        self.image = image
        self.sound = sound

    #The display surface specifications    
    def spawn(self, display_surface):
        self.rect.centerx = random.randrange(100, WINDOW_WIDTH - 100, 64) + 15
        self.rect.centery = random.randrange(100, WINDOW_HEIGHT - 100, 64) + 15
        display_surface.blit(self.image, self.rect)  
    
    #Display surface is updated
    def update(self, display_surface):
        keys = pygame.key.get_pressed() #The system gets keyboard input from the user.
        
        #The soap is movef based on keyboard input
        if keys[K_RIGHT]:
            self.rect.centerx  -= offset

        if keys[K_LEFT]:
            self.rect.centerx  += offset
        display_surface.blit(self.image, self.rect)  