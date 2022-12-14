"""
Dilyana Koleva, July 2022
Space Invaders - Improvements
"""
import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# Background
background = pygame.image.load('background.png')
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('me.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('laser.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10

# Ready - you can't see bullet on the screen
# Fire - bullet is visible
bullet_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Level
level_value = 1
level_font = pygame.font.Font('freesansbold.ttf', 32)
levelX = 600
levelY = 10

# Game Over
game_over = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over = game_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (200, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_level(x, y):
    global score_value
    if score_value <= 10:
        level = level_font.render("Level " + str(1), True, (255, 255, 255))
        screen.blit(level, (x, y))
    elif 10 < score_value < 30:
        level = level_font.render("Level " + str(2), True, (255, 255, 255))
        screen.blit(level, (x, y))
    elif (30) < score_value < 40:
        level = level_font.render("Level " + str(3), True, (255, 255, 255))
        screen.blit(level, (x, y))
    elif 40 <= score_value < 50:
        level = level_font.render("Level " + str(4), True, (255, 255, 255))
        screen.blit(level, (x, y))
    elif 50 <= score_value < 60:
        level = level_font.render("Level " + str(5), True, (255, 255, 255))
        screen.blit(level, (x, y))



def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))  # ensures the bullet is shot from the nose of the spaceship


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2))
                         + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def play():
    player(playerX, playerY)
    show_score(textX, textY)
    show_level(levelX, levelY)
    pygame.display.update()


# Game Loop
def game_loop():
    global score_value, playerX, playerY, playerX_change, \
        bulletY, bulletX, bullet_state, bulletY_change, bulletX_change
    isRunning = True
    while isRunning:

        # Background Image
        screen.blit(background, (0, 0))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                isRunning = False

            # If keystroke is pressed check right or left
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    playerX_change = -5
                if e.key == pygame.K_RIGHT:
                    playerX_change = 5
                if e.key == pygame.K_SPACE:
                    if bullet_state == 'ready':
                        bullet_sound = mixer.Sound("laser.wav")
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                    playerX_change = 0

        # Ensures boundaries of spaceship
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy movement
        for i in range(number_of_enemies):
            if enemyY[i] > 440:
                for j in range(number_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 3
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -3
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound = mixer.Sound("explosion.wav")
                explosion_sound.play()
                bulletY = 480
                bullet_state = 'ready'
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)
            enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = 'ready'
        if bullet_state == 'fire':
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        play()


def main():
    title_font = pygame.font.SysFont("freesansbold.ttf", 60)
    isRunning = True
    while isRunning:
        screen.blit(background, (0, 0))
        title_label = title_font.render("Play", 1, (255, 255, 255))
        screen.blit(title_label, (350, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_loop()
    pygame.quit()


if __name__ == "__main__":
    main()
