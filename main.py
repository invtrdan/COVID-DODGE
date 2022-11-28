import pygame, sys
from pygame import *
from pygame.locals import QUIT
from config import *
from player import Player
from virusx import Virusx
from virusy import Virusy
from mask import Mask
from soap import Soap
import time

pygame.init()
pygame.mixer.init()

#Music is loaded and the volume is set.
pygame.mixer.music.load('tempting_fate.mp3')
pygame.mixer.music.set_volume(0.1)

sound = pygame.mixer.Sound('shimmer_1.ogg')

#This module is responsible for sprite movement. 
def move_items(display_surface, virus_sprites, player_sprites, mask_sprites, soap_sprites, soap_timer, direction, timer):
    for virus in virus_sprites:
        virus_sprites.remove(virus)
        if virus.rect.centerx > WINDOW_WIDTH or virus.rect.centery > WINDOW_HEIGHT or (pygame.sprite.spritecollide(virus, virus_sprites, False) and virus.rect.centerx == 25):
            virus.spawn(display_surface, timer)
        virus_sprites.add(virus)
        virus.move(display_surface)
    for player in player_sprites:
        direction = player.move(display_surface, direction)
    if timer % 150 == 0 and timer != 0:
        mask_sprites = mask_create()
        for mask in mask_sprites:
            mask.spawn(display_surface)
    for mask in mask_sprites:
        mask.update(display_surface)
    if timer % DIFFICULTY_INCREASE == 0 and timer != 0:
        soap_sprites = soap_create()
        for soap in soap_sprites:
            soap.spawn(display_surface)
            soap_timer = 0
    else:
        soap_timer += 1
    if soap_timer == 90:
        for soap in soap_sprites:
            soap_sprites.remove(soap)
    for soap in soap_sprites:
        soap.update(display_surface)
    return direction, mask_sprites, soap_sprites, soap_timer

#This module is responsible for creating the player displayed
def player_create():
    player = Player( CENTERX, CENTERY)
    player_sprites = pygame.sprite.Group()
    player_sprites.add(player)
    direction = 'right'
    return player_sprites, direction

#This module is responsible for creating the masks displayed
def mask_create():
    mask_img = pygame.image.load('mask.png')
    sound = pygame.mixer.Sound('shimmer_1.ogg')
    sound.set_volume(0.1)
    mask_sprites = pygame.sprite.Group()
    mask = Mask(mask_img, sound)
    mask_sprites.add(mask)
    return mask_sprites

#This module is responsible for creating the soap displayed
def soap_create():
    soap_img = pygame.image.load('soap.png')
    soap_img = pygame.transform.scale(soap_img, (40, 40))
    sound = pygame.mixer.Sound('shimmer_1.ogg')
    sound.set_volume(0.1)
    soap_sprites = pygame.sprite.Group()
    soap = Soap(soap_img, sound)
    soap_sprites.add(soap)
    return soap_sprites

#This module is responsible for creating the virus displayed
def virus_create(display_surface, num, timer = 0):
    virus_img = pygame.image.load('Blue_Virus.png')
    virus_img = pygame.transform.scale(virus_img, (36, 36))
    virus_sprites = pygame.sprite.Group()
    for i in range(num):
        virus = Virusx(virus_img)
        virus_sprites.add(virus)
        virus.spawn(display_surface, timer)
        virus = Virusy(virus_img)
        virus_sprites.add(virus)
        virus.spawn(display_surface, timer)
    return virus_sprites

#This module is responsible for creating and displaying the game score.
def score_create(score = 0):
    text = font.render('Score =' + str(score), True, BLUE)  
    text_rect = text.get_rect()
    text_rect.center = (WINDOW_WIDTH - 110, 30) #Position of the score on display screen
    go_text = go_font.render('Game Over! Score = '+ str(score), True, BLUE)
    go_text_rect = go_text.get_rect()
    go_text_rect.center = (CENTERX, CENTERY)
    restart_text = go_font.render('(Press R to restart!)', True, BLUE)
    restart_text_rect = restart_text.get_rect()
    restart_text_rect.center = (CENTERX, CENTERY + 30)
    return text, text_rect, go_text, go_text_rect,  restart_text, restart_text_rect

#This module is responsible for updating the player's score
def update_score(text, go_text, score):
    text = font.render('Score = ' + str(score), True, BLUE)
    go_text = go_font.render('Game Over! Score = ' + str(score) , True, BLUE)
    return text, go_text

#This module is responsible for detecting collisions between the plaer and the virus.
def detect_virus_player_collisions(virus_sprites, player_sprites, invincible):
    results = {}
    if invincible == False:
        for virus in virus_sprites:
            for player in player_sprites:
                if pygame.sprite.spritecollide(player, virus_sprites, False):
                    results[virus] = player
        return results
    else:
        return results
#This module is responsible for detecting collisions between the mask and the player.    
def detect_mask_player_collisions(mask_sprites, player_sprites):
    results = {}
    for mask in mask_sprites:
        for player in player_sprites:
            if pygame.sprite.spritecollide(player, mask_sprites, False):
                results[mask] = player
    return results
#This module is responsible for detecting collisions between the soap and the player.
def detect_soap_player_collisions(soap_sprites, player_sprites):
    results = {}
    for soap in soap_sprites:
        for player in player_sprites:
            if pygame.sprite.spritecollide(player, soap_sprites, False):
                results[soap] = player
    return results

#This module is responsible for removing virus and player items after collision
def remove_collided_items(collision_dictionary, virus_sprites, player_sprites, mask_sprites, lives, invincible):
    if lives == 0:
        for mask in mask_sprites:
            mask_sprites.remove(mask)
        for virus, player in collision_dictionary.items(): # Iterates over the dictionary getting keys and corresponding values
            virus_sprites.remove(virus)
            player_sprites.remove(player)
            pygame.mixer.music.stop()
            GAME_OVER.play()
        return 2, -1, False
    else:
        lives -= 1
        invincible = True
        get_hit.play()
    return 1, lives, invincible

#This module is responsible for removing the soa[ from the screen after collision]
def remove_collided_soap(collision_dictionary, soap_sprites, player_sprites, lives):
    for soap, player in collision_dictionary.items(): # Iterates over the dictionary getting keys and corresponding values
        soap.sound.play()
        soap_sprites.remove(soap)
        lives += 1
    return lives

#This module is responsible for removing the mask after collision
def remove_collided_mask(collision_dictionary, mask_sprites, player_sprites, score):
    for mask, player in collision_dictionary.items(): # Iterates over the dictionary getting keys and corresponding values
        mask.sound.play()
        mask_sprites.remove(mask)
        score += 5
    return score

#This mocule is responsible for displaying the number of lives (hearts) remaining.
def display_lives(lives, display_surface, heart):
    x_value = 15
    for i in range(lives + 1):
        display_surface.blit(heart, [x_value, 15])
        x_value += 35

#This module allows for the player to be invincible for a period of time if the timer < 30
def is_invincible(invincible, i_timer):
    if i_timer < 30 and invincible == True:
        invincible = True
        i_timer += 1
    elif i_timer == 30:
        invincible = False
        i_timer = 0
    return invincible, i_timer
        
       
pygame.init()

# Open a window
DISPLAYSURF = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption('Flatten The Curve') #title of game at the top of game window
virus_img = pygame.image.load('Blue_Virus.png')
virus_img = pygame.transform.scale(virus_img, (32, 32))
pygame.display.set_icon(virus_img) #changes the icon of the game
num = 4
player_list, direction = player_create() #Player create function
virus_list = virus_create(DISPLAYSURF, num)
mask_sprites = pygame.sprite.Group()
soap_sprites = pygame.sprite.Group()
timer = 0
font = pygame.font.Font('freesansbold.ttf', 30) #Font design and size
go_font = pygame.font.Font('freesansbold.ttf', 32)
score = 0
lives = 2
GAME_OVER = pygame.mixer.Sound('GameOver.ogg') #Sound is played when the game is lost/ over
GAME_OVER.set_volume(0.015) #The volume of the game is set
game_state = 0 #The game satate is initialized
text, text_rect, go_text, go_text_rect, restart_text, restart_text_rect = score_create()
animation_increment=10
clock_tick_rate=20
invincible = False
i_timer = 0
offset_x = 0
get_hit = pygame.mixer.Sound('get_hit.ogg')
get_hit.set_volume(0.15)
heart_img = pygame.image.load('Heart.png')
heart_img = pygame.transform.scale(heart_img, (30, 30))
soap_timer = 0
clock = pygame.time.Clock()
background_image = pygame.image.load("road.png") #background image
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
start_screen = pygame.image.load("start_screen.jpeg") #start screen image
start_screen = pygame.transform.scale(start_screen, (WINDOW_WIDTH, WINDOW_HEIGHT))

while game_state == 0:
    keys = pygame.key.get_pressed() #gets input from the keyboard
    DISPLAYSURF.blit(start_screen, [0, 0])
    for event in pygame.event.get(): 
        if event.type == QUIT or keys[K_ESCAPE]: 
            pygame.quit()
            sys.exit() 
        if event.type == pygame.KEYDOWN and not keys[K_ESCAPE] : 
            game_state = 1
            pygame.mixer.music.play(loops = -1)

    pygame.display.update()
    clock.tick(FPS)        
            
while game_state:
 
    timer += 1
    
    keys = pygame.key.get_pressed() #gets keyboard input
    for event in pygame.event.get(): 
        if event.type == QUIT or keys[K_ESCAPE]: 
            pygame.quit()
            sys.exit()
        if keys[K_r]: 
            game_state = 1
            player_list, direction = player_create()
            num = 4
            virus_list = virus_create(DISPLAYSURF, num)
            score = 0
            timer = 0
            offset_x = 0
            i_timer = 0
            lives = 2
            soap_timer = 0
            pygame.mixer.music.play(loops = -1)
            mask_sprites = pygame.sprite.Group()
 
    #Movement depending on keyboad input
    if keys[K_RIGHT]:
        offset_x -= offset

    if keys[K_LEFT]:
        offset_x += offset

    #Display window  
    rel_x = offset_x % WINDOW_WIDTH
    DISPLAYSURF.blit(background_image,[rel_x - WINDOW_WIDTH, 0])
    if rel_x < WINDOW_WIDTH:
        DISPLAYSURF.blit(background_image, [rel_x, 0])
    
    DISPLAYSURF.blit(text, text_rect)

    display_lives(lives, DISPLAYSURF, heart_img) #display lives function is called to display remaining lives
    invincible, i_timer = is_invincible(invincible, i_timer) #invinciple, i_timer is passed to the is_invincible function to determine whether or not the player is invincible.
     
    direction, mask_sprites, soap_sprites, soap_timer = move_items(DISPLAYSURF, virus_list, player_list, mask_sprites, soap_sprites, soap_timer, direction, timer)
        
    vp_collision_dictionary = detect_virus_player_collisions(virus_list, player_list, invincible)
    mp_collision_dictionary = detect_mask_player_collisions(mask_sprites, player_list)
    sp_collision_dictionary = detect_mask_player_collisions(soap_sprites, player_list)
    
    #Colided items are removed    
    if vp_collision_dictionary:
        game_state, lives, invincible = remove_collided_items(vp_collision_dictionary, virus_list, player_list, mask_sprites, lives, invincible)
    
    #function called to remove maks after collision
    if mp_collision_dictionary:
        score = remove_collided_mask(mp_collision_dictionary, mask_sprites, player_list, score)
    
    #Function cslled to remove soap after collision
    if sp_collision_dictionary:
        lives = remove_collided_soap(sp_collision_dictionary, soap_sprites, player_list, lives)
            
    text, go_text = update_score(text, go_text, score)
    
    #The difficulty is increased by increasing speed
    if timer % 30 == 0 and game_state != 2:
        if timer % DIFFICULTY_INCREASE == 0 and timer != 0 and num < 8:
            num += 1
            virus_list = virus_create(DISPLAYSURF, num, timer)
        score += 1
    #Restart option    
    if game_state == 2:
        DISPLAYSURF.blit(go_text, go_text_rect)
        DISPLAYSURF.blit(restart_text, restart_text_rect)
    
    pygame.display.update()
    clock.tick(FPS) 
