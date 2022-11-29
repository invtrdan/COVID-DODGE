from config import *
import pygame, random
from pygame.locals import *

#########################################
#              Soap Class               #
#########################################
class Soap(pygame.sprite.Sprite):

    def __init__(self, image, sound):
        super().__init__()
        self.rect = image.get_rect()
        self.image = image
        self.sound = sound
   
    def spawn(self, display_surface):
        self.rect.centerx = random.randrange(100, WINDOW_WIDTH - 100, 64) + 15
        self.rect.centery = random.randrange(100, WINDOW_HEIGHT - 100, 64) + 15
        display_surface.blit(self.image, self.rect)  
    
    def update(self, display_surface):
        keys = pygame.key.get_pressed() 

        if keys[K_RIGHT]:
            self.rect.centerx  -= offset

        if keys[K_LEFT]:
            self.rect.centerx  += offset
        display_surface.blit(self.image, self.rect)  