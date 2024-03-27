import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
WHITE = (245, 245, 245)
BLACK = (10, 10, 10)

# Player
player_width = 50
player_height = 50
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5

# Bullet
bullet_height = 20
bullet_width = 50
bullet_color = WHITE
bullet_speed = 7
bullets = []
bullet_cooldown = 0.2  # cooldown
last_shot_time = 0

# Enemy
enemy_width = 50
enemy_height = 50
enemy_speed = 3
max_enemies = 2  # max num
enemies = []

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(None, 36)
kills = 0

# Load bullet image
bullet_image = pygame.transform.scale(pygame.image.load("bullet.png").convert_alpha(), (bullet_width, bullet_height))
def rotate_bullet():
    global bullet_image
    bullet_image = pygame.transform.rotate(bullet_image, -90)
rotate_bullet()    

# Functions
def winning_condition():
    screen.fill(BLACK)
    global kills
    winner_text = font.render("Winner Winner Chicken Dinner!", True, WHITE)
    screen.blit(winner_text, (screen_width // 2 - winner_text.get_width() // 2, screen_height // 2 - winner_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    kills = 0

def draw_player(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, player_width, player_height))

def draw_bullet(x, y):
    screen.blit(bullet_image, (x, y))

def draw_enemy(x, y):
    pygame.draw.circle(screen, WHITE, (x + enemy_width // 2, y + enemy_height // 2), enemy_width // 2)

def move_bullets():
    global bullets
    bullets = [[bx, by - bullet_speed] for bx, by in bullets if by > 0]

def move_enemies():
    global enemies
    enemies = [[ex, ey + enemy_speed] for ex, ey in enemies if ey < screen_height]
    if len(enemies) < max_enemies:
        generate_enemy()

def generate_enemy():
    enemy_x = random.randint(0, screen_width - enemy_width)
    enemy_y = 0 - enemy_height
    enemies.append([enemy_x, enemy_y])

def check_collision():
    global kills, bullets, enemies  # Add global declaration for bullets and enemies
    collision = False
    to_remove_bullets = []
    to_remove_enemies = []
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
            if bullet_rect.colliderect(enemy_rect):
                to_remove_bullets.append(bullet)
                to_remove_enemies.append(enemy)
                collision = True
    bullets = [bullet for bullet in bullets if bullet not in to_remove_bullets]
    enemies = [enemy for enemy in enemies if enemy not in to_remove_enemies]

    if collision:
        kills += 1
    return collision

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    current_time = pygame.time.get_ticks() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if current_time - last_shot_time > bullet_cooldown:
                bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])
                last_shot_time = current_time

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_d] and player_x < screen_width - player_width:
        player_x += player_speed

    move_bullets()
    move_enemies()

    for bullet in bullets:
        draw_bullet(*bullet)

    for enemy in enemies:
        draw_enemy(*enemy)

    draw_player(player_x, player_y)

    if check_collision():
        pass

    # kill counter
    kill_text = font.render("Kills: " + str(kills), True, WHITE)
    screen.blit(kill_text, (10, 10))

    if kills == 5:
        winning_condition()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
