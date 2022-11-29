import pygame, random
from pygame.locals import *
from config import *

#########################################
#         Virus Class (X-axis)          #
#########################################
class Virusx(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()
        self.rect = image.get_rect()
        self.image = image
        self.vel = 10
     
    def spawn(self, display_surface, timer):
        self.rect.centerx = 0
        self.rect.centery = random.randrange(10, WINDOW_HEIGHT - 40, 64) + 15
        display_surface.blit(self.image, self.rect)  
        if timer % DIFFICULTY_INCREASE == 0 and timer != 0:
            self.vel += 1
   
    def move(self, display_surface):
        self.rect.centerx += self.vel
        keys = pygame.key.get_pressed() 
      
        if keys[K_RIGHT]:
            self.rect.centerx -= self.vel - offset 
        if keys[K_LEFT]:
            self.rect.centerx +=  offset - (self.vel - 10)
        display_surface.blit(self.image, self.rect)  
            
