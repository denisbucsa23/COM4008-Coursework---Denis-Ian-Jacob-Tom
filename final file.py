import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alien Attack")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Load assets
player_img = pygame.image.load('defender.png')
invader_img = pygame.image.load('invader1.png')
laser_sound = pygame.mixer.Sound('laser.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')

# Scale down images
player_img = pygame.transform.scale(player_img, (50, 50))
invader_img = pygame.transform.scale(invader_img, (40, 40))

# Player properties
player_speed = 5
player_width, player_height = player_img.get_size()
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10

# Invader properties
invaders = []
invader_speed = 2
num_invaders = 10
invader_width, invader_height = invader_img.get_size()

# Bullet properties
bullets = []
default_bullet_speed = 7
bullet_speed = default_bullet_speed
default_bullet_height = 10
bullet_width, bullet_height = 5, default_bullet_height

# Invader bullets
invader_bullets = []
invader_bullet_speed = 7

# Game Variables
score = 0
high_score = 0
game_over = False
wave = 1

# Font
font = pygame.font.Font(None, 36)

# Create a starry background
stars = [{"x": random.randint(0, SCREEN_WIDTH), "y": random.randint(0, SCREEN_HEIGHT)} for _ in range(100)]

# Functions
def create_invaders():
    invaders.clear()
    for i in range(5):  # 5 rows
        for j in range(num_invaders):
            x = 50 + j * (invader_width + 30)
            y = 50 + i * (invader_height + 20)
            invaders.append({"x": x, "y": y, "direction": 1})

def draw_player(x, y):
    screen.blit(player_img, (x, y))

def draw_invaders():
    for invader in invaders:
        screen.blit(invader_img, (invader["x"], invader["y"]))

def move_invaders():
    global game_over
    for invader in invaders:
        invader["x"] += invader["direction"] * invader_speed
        # Change direction at screen edge
        if invader["x"] <= 0 or invader["x"] >= SCREEN_WIDTH - invader_width:
            invader["direction"] *= -1
            invader["y"] += 10
            if invader["y"] >= player_y - invader_height:
                game_over = True

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, RED, pygame.Rect(bullet["x"], bullet["y"], bullet_width, bullet_height))

    for bullet in invader_bullets:
        pygame.draw.rect(screen, GREEN, pygame.Rect(bullet["x"], bullet["y"], bullet_width, bullet_height))

def move_bullets():
    for bullet in bullets:
        bullet["y"] -= bullet_speed
    for bullet in invader_bullets:
        bullet["y"] += invader_bullet_speed

    # Remove off-screen bullets
    bullets[:] = [b for b in bullets if b["y"] > 0]
    invader_bullets[:] = [b for b in invader_bullets if b["y"] < SCREEN_HEIGHT]

def handle_collisions():
    global score, game_over, high_score
    for bullet in bullets[:]:
        for invader in invaders[:]:
            if bullet["x"] in range(invader["x"], invader["x"] + invader_width) and \
               bullet["y"] in range(invader["y"], invader["y"] + invader_height):
                bullets.remove(bullet)
                invaders.remove(invader)
                score += 10
                explosion_sound.play()
                high_score = max(high_score,score)
                break

    for bullet in invader_bullets:
        if bullet["x"] in range(player_x, player_x + player_width) and \
           bullet["y"] in range(player_y, player_y + player_height):
            game_over = True

def display_score():
    #ian visnevschi change:
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    wave_text  = font.render(f"Wave:{wave}",True,WHITE)
    screen.blit(high_score_text,(10,40))
    screen.blit(wave_text, (10,70))
    screen.blit(score_text, (10, 10))

def display_game_over():
    game_over_text = font.render("GAME OVER", True, RED)
    restart_text = font.render("Press R to Restart", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 50))

def draw_starry_background():
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star["x"], star["y"]), 2)
        star["y"] += 1
        if star["y"] > SCREEN_HEIGHT:
            star["y"] = 0
            star["x"] = random.randint(0, SCREEN_WIDTH)

# Game loop
create_invaders()
while True:
    screen.fill(BLACK)
    draw_starry_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_SPACE] and len(bullets) < 5:
        bullets.append({"x": player_x + player_width // 2 - bullet_width // 2, "y": player_y})
        laser_sound.play()
    if game_over and keys[pygame.K_r]:
        player_x = SCREEN_WIDTH // 2 - player_width // 2
        player_y = SCREEN_HEIGHT - player_height - 10
        bullets.clear()
        invader_bullets.clear()
        invaders.clear()
        create_invaders()
        score = 0
        wave = 1
        invader_speed = 2
        bullet_speed = default_bullet_speed
        bullet_height = default_bullet_height
        active_power_up = None
        game_over = False

    if not game_over:
        move_invaders()
        move_bullets()
        handle_collisions()

        draw_player(player_x, player_y)
        draw_invaders()
        draw_bullets()
        display_score()

        if not invaders:
            wave += 1
            invader_speed += 2
            create_invaders()
    else:
        display_game_over()

    pygame.display.flip()
    clock.tick(FPS)