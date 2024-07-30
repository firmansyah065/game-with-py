import pygame
import random
import sys
import os

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

player_width = 200
player_height = 200
player_speed = 5
player_move_speed = 5

bullet_width = 10
bullet_height = 15
bullet_speed = 10
bullet_state = "ready"
bullet_x = 0  
bullet_y = 0  

enemy_width = 100
enemy_height = 100
enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
enemy_y = random.randint(-500, -50)
enemy_speed = 3

font = pygame.font.Font(None, 36)
score = 0
highscore = 0

# Muat gambar latar belakang
bg_image_path = r'C:\Users\Administrator\Documents\project sentra\iseng\a76408f06cac0061f1cef61e420827e3.jpg'

if not os.path.isfile(bg_image_path):
    print(f"File {bg_image_path} tidak ditemukan.")
    pygame.quit()
    sys.exit()

background_image = pygame.image.load(bg_image_path)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Muat gambar pesawat
player_image_path = r'C:\Users\Administrator\Documents\project sentra\iseng\_Pngtree_vector_airplane_icon_4277896-removebg-preview.png'
if not os.path.isfile(player_image_path):
    print(f"File {player_image_path} tidak ditemukan.")
    pygame.quit()
    sys.exit()

player_image = pygame.image.load(player_image_path)
player_image = pygame.transform.scale(player_image, (player_width, player_height))
player_rect = player_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70))

# Muat gambar pesawat musuh
enemy_image_path = r'C:\Users\Administrator\Documents\project sentra\iseng\PESAWATMUSUH.png'
if not os.path.isfile(enemy_image_path):
    print(f"File {enemy_image_path} tidak ditemukan.")
    pygame.quit()
    sys.exit()

enemy_image = pygame.image.load(enemy_image_path)
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))
enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def reset_game():
    global player_rect, enemy_x, enemy_y, bullet_state, score, game_over, enemy_rect
    player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70)
    enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
    enemy_y = random.randint(-500, -50)
    bullet_state = "ready"
    score = 0
    game_over = False
    enemy_rect.topleft = (enemy_x, enemy_y)

running = True
game_over = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_w:
                if bullet_state == "ready":
                    bullet_state = "fire"
                    bullet_x = player_rect.centerx - bullet_width // 2
                    bullet_y = player_rect.top
            elif event.key == pygame.K_SPACE and game_over:
                reset_game()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_a]:
            player_rect.x -= player_speed
        if keys[pygame.K_d]:
            player_rect.x += player_speed
        if keys[pygame.K_p]:
            player_rect.x += player_move_speed
        if keys[pygame.K_k]:
            player_rect.x -= player_move_speed

        if player_rect.x < 0:
            player_rect.x = 0
        if player_rect.x > SCREEN_WIDTH - player_width:
            player_rect.x = SCREEN_WIDTH - player_width

        enemy_y += enemy_speed
        enemy_rect.topleft = (enemy_x, enemy_y)

        if bullet_state == "fire":
            bullet_y -= bullet_speed

        if bullet_y <= 0:
            bullet_state = "ready"

        if bullet_state == "fire" and enemy_rect.colliderect(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)):
            bullet_state = "ready"
            score += 1
            enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
            enemy_y = random.randint(-500, -50)

        if player_rect.colliderect(enemy_rect):
            game_over = True
            if score > highscore:
                highscore = score

        if enemy_y > SCREEN_HEIGHT:
            enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
            enemy_y = random.randint(-500, -50)
            game_over = True
            if score > highscore:
                highscore = score

    screen.blit(background_image, (0, 0))
    screen.blit(player_image, player_rect.topleft)
    screen.blit(enemy_image, enemy_rect.topleft)

    if bullet_state == "fire":
        pygame.draw.rect(screen, WHITE, (bullet_x, bullet_y, bullet_width, bullet_height))

    draw_text(f"Score: {score}", font, WHITE, 70, 30)
    draw_text(f"Highscore: {highscore}", font, WHITE, SCREEN_WIDTH - 120, 30)

    if game_over:
        draw_text("Press SPACE to play again", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    draw_text("BY: MR.BLEGEDES065", font, WHITE, 135, SCREEN_HEIGHT - 20)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
