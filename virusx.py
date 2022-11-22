import pygame, random
from pygame.locals import *
from config import *

#The virus class for the x axis directions (left to right)
class Virusx(pygame.sprite.Sprite):
    
    #The virusx is initialized
    def __init__(self, image):
        super().__init__()
        self.rect = image.get_rect()
        self.image = image
        self.vel = 10
    
    #The virusx is spawned    
    def spawn(self, display_surface, timer):
        self.rect.centerx = 0
        self.rect.centery = random.randrange(10, WINDOW_HEIGHT - 40, 64) + 15
        display_surface.blit(self.image, self.rect)  
        if timer % DIFFICULTY_INCREASE == 0 and timer != 0:
            self.vel += 1
    #Whe virusx is moved        
    def move(self, display_surface):
        self.rect.centerx += self.vel
        keys = pygame.key.get_pressed() #The program reads keyboard input from the user
        #The virus is moved based on used keyboard input.
        if keys[K_RIGHT]:
            self.rect.centerx -= self.vel - offset 
        if keys[K_LEFT]:
            self.rect.centerx +=  offset - (self.vel - 10)
        display_surface.blit(self.image, self.rect)  
            
