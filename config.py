import pygame

#COnstants are keyp here
BLUE = (0, 0, 255)  
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 768  #The 
WINDOW_HEIGHT = 768 #The value of the window height is stored here
CENTERX = WINDOW_WIDTH // 2
CENTERY = WINDOW_HEIGHT // 2
FPS = 30 
fpsClock = pygame.time.Clock()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
ACC = 1.4 #The acceleration value is stored here
DIFFICULTY_INCREASE = 600 #The speed can be adjusted here
offset = 8