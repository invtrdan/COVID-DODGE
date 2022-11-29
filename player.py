import pygame
from os import path
from pygame.locals import *
from config import *
from pygame.math import Vector2

#########################################
#             Player Class              #
#########################################
class Player(pygame.sprite.Sprite):
    
    def __init__(self, startx, starty):
        super().__init__()
        self.load_images() 
        self.image = self.run_images[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = startx
        self.rect.centery = starty 
        self.current_frame = 0
        self.is_running = False
        self.position = Vector2(startx, starty) 
        self.velocity = Vector2(0, 0) 
        self.acceleration = Vector2(0, 0) 
      
    def move(self, display_surface, direction):
        self.animate()
        self.acceleration = Vector2(0, 0) 
        self.is_running = False
        
        if direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)    
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.centerx > 10:
            self.is_running = True
            direction = 'left'
            self.acceleration.x = -ACC 
        if keys[K_RIGHT] and self.rect.centerx:
            self.is_running = True
            direction = 'right'
            self.acceleration.x = ACC
        if keys[K_UP] and self.rect.centery>10:
            self.is_running = True
            self.acceleration.y = -ACC
        if keys[K_DOWN] and self.rect.centery <WINDOW_HEIGHT - 40:
            self.is_running = True
            self.acceleration.y = ACC
        
        self.acceleration += -0.15 * self.velocity 
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        if self.position.x > WINDOW_WIDTH - 20:
            self.position.x = WINDOW_WIDTH - 20
        if self.position.x < 20:
            self.position.x = 20
        if self.position.y > WINDOW_HEIGHT - 20:
            self.position.y = WINDOW_HEIGHT - 20
        if self.position.y < 20:
            self.position.y = 20   
        self.rect.center = self.position
        display_surface.blit(self.image, self.rect)
        return direction
    
    def animate(self):
        if self.is_running:
            self.current_frame = (self.current_frame + 1) % len(self.run_images)
            self.image = self.run_images[self.current_frame]
        else:
            self.current_frame = 30
            self.image = self.run_images[self.current_frame]
            
    def load_images(self):
        img_dir = path.join(path.dirname(__file__), 'img')
        images = ['run_000.png', 'run_001.png', 'run_002.png', 'run_003.png', \
                  'run_004.png', 'run_005.png', 'run_006.png', 'run_007.png', \
                  'run_008.png', 'run_009.png', 'run_010.png', 'run_011.png', \
                  'run_012.png', 'run_013.png', 'run_014.png', 'run_015.png', \
                  'run_016.png', 'run_017.png', 'run_018.png', 'run_019.png', \
                  'run_020.png', 'run_021.png', 'run_022.png', 'run_023.png', \
                  'run_024.png', 'run_025.png', 'run_026.png', 'run_027.png', \
                  'run_028.png', 'run_029.png', 'run_030.png', 'run_031.png', \
                  'run_032.png', 'run_033.png', 'run_034.png', 'run_035.png', \
                  'run_036.png', 'run_037.png', 'run_038.png', 'run_039.png', \
                  'run_040.png', 'run_041.png', 'run_042.png']
        self.run_images = []
        
        for image in images:
            self.run_images.append(pygame.transform.scale((pygame.image.load(path.join(img_dir, image))), (60, 60)))