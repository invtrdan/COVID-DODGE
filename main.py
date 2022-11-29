import pygame, sys, time, requests, json
from pygame import *
from pygame.locals import QUIT
from config import *
from player import Player
from virusx import Virusx
from virusy import Virusy
from mask import Mask
from soap import Soap

#########################################
#               Play Game               #
#########################################
BASE_URL = "https://covid-dodge-server.invtrdan.repl.co"

def play_game(username):
  pygame.init()
  pygame.mixer.init()
  
  pygame.mixer.music.load('tempting_fate.mp3')
  pygame.mixer.music.set_volume(0.1)
  sound = pygame.mixer.Sound('shimmer_1.ogg')
  
  #########################################
  #            Sprite Movement            #
  #########################################
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
  
  #########################################
  #                Player                 #
  #########################################
  def player_create():
      player = Player( CENTERX, CENTERY)
      player_sprites = pygame.sprite.Group()
      player_sprites.add(player)
      direction = 'right'
      return player_sprites, direction
  
  #########################################
  #                 Masks                 #
  #########################################           
  def mask_create():
      mask_img = pygame.image.load('mask.png')
      sound = pygame.mixer.Sound('shimmer_1.ogg')
      sound.set_volume(0.1)
      mask_sprites = pygame.sprite.Group()
      mask = Mask(mask_img, sound)
      mask_sprites.add(mask)
      return mask_sprites
  
  #########################################
  #                 Soap                  #
  #########################################
  def soap_create():
      soap_img = pygame.image.load('soap.png')
      soap_img = pygame.transform.scale(soap_img, (40, 40))
      sound = pygame.mixer.Sound('shimmer_1.ogg')
      sound.set_volume(0.1)
      soap_sprites = pygame.sprite.Group()
      soap = Soap(soap_img, sound)
      soap_sprites.add(soap)
      return soap_sprites
  
  #########################################
  #                 Virus                 #
  #########################################
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
  
  #########################################
  #                 Score                 #
  #########################################
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
  
  #########################################
  #             Update Score              #
  #########################################
  def update_score(text, go_text, score):
      text = font.render('Score = ' + str(score), True, BLUE)
      go_text = go_font.render('Game Over! Score = ' + str(score) , True, BLUE)
      return text, go_text
  
  #########################################
  #          Collision Detection          #
  #########################################
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
          
  def detect_mask_player_collisions(mask_sprites, player_sprites):
      results = {}
      for mask in mask_sprites:
          for player in player_sprites:
              if pygame.sprite.spritecollide(player, mask_sprites, False):
                  results[mask] = player
      return results
    
  def detect_soap_player_collisions(soap_sprites, player_sprites):
      results = {}
      for soap in soap_sprites:
          for player in player_sprites:
              if pygame.sprite.spritecollide(player, soap_sprites, False):
                  results[soap] = player
      return results
  
  def remove_collided_items(collision_dictionary, virus_sprites, player_sprites, mask_sprites, lives, invincible):
      if lives == 0:
          for mask in mask_sprites:
              mask_sprites.remove(mask)
          for virus, player in collision_dictionary.items(): 
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
  
  def remove_collided_soap(collision_dictionary, soap_sprites, player_sprites, lives):
      for soap, player in collision_dictionary.items(): 
          soap.sound.play()
          soap_sprites.remove(soap)
          lives += 1
      return lives
  
  def remove_collided_mask(collision_dictionary, mask_sprites, player_sprites, score):
      for mask, player in collision_dictionary.items(): 
          mask.sound.play()
          mask_sprites.remove(mask)
          score += 5
      return score

  #########################################
  #                 Lives                 #
  #########################################
  def display_lives(lives, display_surface, heart):
      x_value = 15
      for i in range(lives + 1):
          display_surface.blit(heart, [x_value, 15])
          x_value += 35
  
  #########################################
  #             Invincibility             #
  #########################################
  def is_invincible(invincible, i_timer):
      if i_timer < 30 and invincible == True:
          invincible = True
          i_timer += 1
      elif i_timer == 30:
          invincible = False
          i_timer = 0
      return invincible, i_timer
      
  pygame.init()
  DISPLAYSURF = pygame.display.set_mode(size, pygame.FULLSCREEN)
  pygame.display.set_caption('Flatten The Curve') 
  virus_img = pygame.image.load('Blue_Virus.png')
  virus_img = pygame.transform.scale(virus_img, (32, 32))
  pygame.display.set_icon(virus_img) 
  num = 4
  player_list, direction = player_create()
  virus_list = virus_create(DISPLAYSURF, num)
  mask_sprites = pygame.sprite.Group()
  soap_sprites = pygame.sprite.Group()
  timer = 0
  font = pygame.font.Font('freesansbold.ttf', 30) 
  go_font = pygame.font.Font('freesansbold.ttf', 32)
  score = 0
  lives = 2
  GAME_OVER = pygame.mixer.Sound('GameOver.ogg') 
  GAME_OVER.set_volume(0.015) 
  game_state = 0 
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
  background_image = pygame.image.load("road.png") 
  background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
  
  start_screen = pygame.image.load("start_screen.jpeg") 
  start_screen = pygame.transform.scale(start_screen, (WINDOW_WIDTH, WINDOW_HEIGHT))

  end_screen = pygame.image.load("game_over.jpeg") 
  end_screen = pygame.transform.scale(end_screen, (WINDOW_WIDTH, WINDOW_HEIGHT))
  
  while game_state == 0:
      keys = pygame.key.get_pressed() 
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
      keys = pygame.key.get_pressed() 
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
   
      #########################################
      #            Sprite Movement            #
      #########################################
      if keys[K_RIGHT]:
          offset_x -= offset
  
      if keys[K_LEFT]:
          offset_x += offset
  
      #########################################
      #                Display                #
      #########################################
      rel_x = offset_x % WINDOW_WIDTH
      DISPLAYSURF.blit(background_image,[rel_x - WINDOW_WIDTH, 0])
      if rel_x < WINDOW_WIDTH:
          DISPLAYSURF.blit(background_image, [rel_x, 0])
      DISPLAYSURF.blit(text, text_rect)
  
      display_lives(lives, DISPLAYSURF, heart_img) 
      invincible, i_timer = is_invincible(invincible, i_timer) 
       
      direction, mask_sprites, soap_sprites, soap_timer = move_items(DISPLAYSURF, virus_list, player_list, mask_sprites, soap_sprites, soap_timer, direction, timer)
          
      vp_collision_dictionary = detect_virus_player_collisions(virus_list, player_list, invincible)
      mp_collision_dictionary = detect_mask_player_collisions(mask_sprites, player_list)
      sp_collision_dictionary = detect_mask_player_collisions(soap_sprites, player_list)
          
      if vp_collision_dictionary:
          game_state, lives, invincible = remove_collided_items(vp_collision_dictionary, virus_list, player_list, mask_sprites, lives, invincible)
      
      if mp_collision_dictionary:
          score = remove_collided_mask(mp_collision_dictionary, mask_sprites, player_list, score)
      
      if sp_collision_dictionary:
          lives = remove_collided_soap(sp_collision_dictionary, soap_sprites, player_list, lives)
              
      text, go_text = update_score(text, go_text, score)
      
      #The difficulty is increased by increasing speed
      # if timer % 30 == 0 and game_state != 2:
      #     if timer % DIFFICULTY_INCREASE == 0 and timer != 0 and num < 8:
      #         num += 1
      #         virus_list = virus_create(DISPLAYSURF, num, timer)
      #     score += 1
        
      #########################################
      #                Restart                #
      #########################################    
      if game_state == 2:
        DISPLAYSURF.blit(go_text, go_text_rect)
        DISPLAYSURF.blit(restart_text, restart_text_rect)

        data = {
          "username":username,
          "score":score
        }
        requests.post(BASE_URL + "/update_leaderboard", json=data)
        
        start_game()
      
      pygame.display.update()
      clock.tick(FPS) 

def start_game():
  username = "Danielle"
  play_game(username)

start_game()



