# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 13:04:11 2020

@author: User
"""
from config import *
import pygame, random
from pygame.locals import *

#Mask class is created
class Mask(pygame.sprite.Sprite):
    
    def __init__(self, image, sound):
        super().__init__()
        self.rect = image.get_rect()
        self.image = image
        self.sound = sound

    #Mask dimensions are set    
    def spawn(self, display_surface):
        self.rect.centerx = random.randrange(100, WINDOW_WIDTH - 100, 64) + 15
        self.rect.centery = random.randrange(100, WINDOW_HEIGHT - 100, 64) + 15
        display_surface.blit(self.image, self.rect)  
    
    #Mask state is updated based on key input
    def update(self, display_surface):
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            self.rect.centerx  -= offset

        if keys[K_LEFT]:
            self.rect.centerx  += offset
        display_surface.blit(self.image, self.rect)  