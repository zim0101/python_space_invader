import os
import pygame

# assets loading and fonts
BACKGROUND = pygame.image.load(os.path.join("assets", "background.jpg"))
PLAYER_IMAGE = pygame.image.load(os.path.join("assets", "spaceship.png"))
RED_ENEMY_IMAGE = pygame.image.load(os.path.join("assets", "red-enemy.png"))
BULLET = pygame.image.load(os.path.join("assets", "bullet.png"))

explosion_sound = pygame.mixer.Sound(os.path.join("assets",
                                                  "explosion.WAV"))
font = pygame.font.Font("freesansbold.ttf", 20)
game_over_font = pygame.font.Font("freesansbold.ttf", 70)
