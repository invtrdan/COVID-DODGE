import pygame, random
from pygame.locals import *
from config import *

#########################################
#         Virus Class (Y-axis)          #
#########################################
class Virusy(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__() 
        self.rect = image.get_rect()
        self.image = image
        self.vel = 10
          
    def spawn(self, display_surface, timer):
        self.rect.centerx = random.randrange(10,WINDOW_WIDTH  - 40, 64) + 40
        self.rect.centery = 0
        display_surface.blit(self.image, self.rect)  
        if timer % DIFFICULTY_INCREASE == 0 and timer != 0:
            self.vel += 1
                
    def move(self, display_surface):
        self.rect.centery += self.vel
        display_surface.blit(self.image, self.rect)  
            
