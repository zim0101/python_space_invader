import os
import random
import math
import pygame
from properties import *

pygame.mixer.pre_init(frequency=44100)
pygame.init()
pygame.mixer.init(frequency=44100)

if __name__ == "__main__":

    # window config
    window_height = 800
    window_width = 800

    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('War Ship')
    game_icon = pygame.image.load(os.path.join("assets", "icon.png"))
    pygame.display.set_icon(game_icon)

    # scoring
    score = 0
    life = 100
    winning_score = 1000
    ammo = winning_score * 1000

    # player
    player_x = 350
    player_y = 730
    player_velocity = 3

    # enemy ships
    enemy_image = []
    enemy_x = []
    enemy_y = []
    enemy_velocity = []
    enemy_number = 10
    for i in range(0, enemy_number):
        enemy_image.append(RED_ENEMY_IMAGE)
        enemy_x.append(random.randint(70, 730))
        enemy_y.append(70)
        enemy_velocity.append(random.uniform(0.1, 0.5))

    # bullet
    bullet_x = 0
    bullet_y = 750
    bullet_velocity = 30
    bullet_state = "ready"

    # actions
    def show_score():
        score_text = font.render("Score : " + str(score), True, (255, 255, 255))
        ammo_text = font.render("Ammo : " + str(ammo), True, (255, 255, 255))
        color = (255, 255, 255)
        if 100 > life >= 60:
            color = (14, 214, 0)
        if 60 > life > 40:
            color = (177, 184, 0)
        if 40 > life >= 0:
            color = (184, 0, 0)

        life_text = font.render("Life : " + str(life), True, color)
        window.blit(score_text, (10, 10))
        window.blit(ammo_text, (400, 10))
        window.blit(life_text, (600, 10))

    def player(x, y):
        window.blit(PLAYER_IMAGE, (x, y))


    def enemy(x, y, nth_enemy):
        window.blit(enemy_image[nth_enemy], (x, y))


    def trigger_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        window.blit(BULLET, (x + 10, y + 10))


    def collision(ex, ey, bx, by):
        distance = math.sqrt(math.pow((ex - bx), 2) + math.pow((ey - by), 2))
        if distance < 30:
            explosion_sound.play()
            return True
        return False

    def game_over_text():
        text = font.render("GAME OVER", True, (255, 255, 255))
        window.blit(text, (400, 400))

    def winner_text():
        text = font.render("YOY WIN", True, (184, 0, 0))
        window.blit(text, (400, 400))

    # Game Loop

    run = True
    while run:
        window.fill((0, 0, 0))
        window.blit(BACKGROUND, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_x > player_velocity:
            player_x -= player_velocity
        if keys[pygame.K_RIGHT] and player_x < (window_width - 64 -
                                                player_velocity):
            player_x += player_velocity
        if keys[pygame.K_SPACE]:
            if bullet_state is "ready" and ammo > 0:
                print("FIRE IN THE HOLE!")
                ammo -= 1
                bullet_sound = pygame.mixer.Sound(
                    os.path.join("assets", "GUNSHOT.WAV"))
                bullet_sound.play()
                bullet_x = player_x
                trigger_bullet(bullet_x, bullet_y)

                if ammo == 0:
                    game_over_text()
                    run = False

        if bullet_y <= 0:
            bullet_y = 750
            bullet_state = "ready"

        if bullet_state == "fire":
            trigger_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_velocity

        for j in range(0, enemy_number):
            if enemy_y[j] >= 750:
                life -= 10
                if life == 0:
                    game_over_text()
                    run = False
                enemy_y[j] = 10

            enemy_y[j] += enemy_velocity[j]

            if collision(enemy_x[j], enemy_y[j], bullet_x, bullet_y):
                print("ENEMY DESTROYED")
                score += 10
                if score >= winning_score:
                    winner_text()
                    run = False
                bullet_y = 750
                bullet_state = "ready"
                enemy_x[j] = random.randint(70, 730)
                enemy_y[j] = 10

            if collision(enemy_x[j], enemy_y[j], player_x, player_y):
                game_over_text()
                run = False

            enemy(enemy_x[j], enemy_y[j], j)

        player(player_x, player_y)
        show_score()

        pygame.display.update()

pygame.quit()
