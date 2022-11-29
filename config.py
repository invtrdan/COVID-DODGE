import pygame

#Constants
BLUE = (0, 0, 255)  
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 768  
WINDOW_HEIGHT = 768 
CENTERX = WINDOW_WIDTH // 2
CENTERY = WINDOW_HEIGHT // 2
FPS = 30 
fpsClock = pygame.time.Clock()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
ACC = 1.4 
DIFFICULTY_INCREASE = 600 
offset = 8