import pygame
import sys

pygame.init()


# Player class
class Player:
    def __init__(self, x, y, img, l, h):
        self.x = x
        self.y = y
        self.img = img
        self.l = l
        self.h = h
        self.img = pygame.transform.scale(img, (l, h))
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h)

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h)


# Invader class
class Invader:
    def __init__(self, x, y, img, l, h, score=0):
        self.x = x
        self.y = y
        self.img = img
        self.l = l
        self.h = h
        self.img = pygame.transform.scale(img, (l, h))
        self.score = score
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h)

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h)


# Bullet class
class Bullet:
    def __init__(self, x, y, w, h, s):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.speed = s
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


# Screen dimensions
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600
screen = pygame.display.set_mode([SCREEN_HEIGHT, SCREEN_WIDTH])
clock = pygame.time.Clock()  # to slow down the speed of movement
FPS = 30  # Slowed down FPS to make invaders move slower

# Player setup
player = Player((SCREEN_WIDTH / 2) - (35 / 2), (SCREEN_HEIGHT - 100), pygame.image.load("defender.png"), 50, 60)

# Invader setup
invaders = []
for row in range(100, 200, 40):  # Y positions for invaders
    for col in range(100, 500, 40):  # X positions for invaders
        invader = Invader(col, row, pygame.image.load("invader1.png"), 30, 30)
        invaders.append(invader)

# Bullet list
bullets = []

# Invader movement variables
moveRight = True


# Functions to move and draw invaders
def draw_invaders():
    for invader in invaders:
        screen.blit(invader.img, (invader.x, invader.y))


def move_invaders():
    global moveRight
    if moveRight:
        for invader in invaders:
            invader.x += 2  # Slowed down invader movement
        if invaders[-1].x > SCREEN_WIDTH - 30:  # Hit the right edge
            moveRight = False
            for invader in invaders:
                invader.y += 20
    else:
        for invader in invaders:
            invader.x -= 2  # Slowed down invader movement
        if invaders[0].x < 0:  # Hit the left edge
            moveRight = True
            for invader in invaders:
                invader.y += 20


# Game loop
running = True
game_over = False  # To track game-over status
font = pygame.font.Font(None, 36)  # For rendering text

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x -= 5
            elif event.key == pygame.K_RIGHT:
                player.x += 5
            elif event.key == pygame.K_SPACE:
                # Allow firing multiple bullets
                bullet = Bullet(player.x + 12, player.y, 10, 20, 10)
                bullets.append(bullet)

    if game_over:
        # Game over message
        screen.fill([0, 0, 0])  # black background
        game_over_text = font.render("Game Over! Press ESC to quit.", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH / 2 - game_over_text.get_width() / 2, SCREEN_HEIGHT / 2))
        pygame.display.flip()
        continue  # Skip the rest of the game loop during game over

    # Screen update
    screen.fill([0, 0, 0])  # black background

    # Move and draw invaders
    move_invaders()
    draw_invaders()

    # Draw player
    screen.blit(player.img, (player.x, player.y))

    # Update and draw bullets
    for bullet in bullets[:]:
        pygame.draw.rect(screen, [0, 255, 0], bullet.rect)
        bullet.y -= bullet.speed
        bullet.update()
        if bullet.y < 0:
            bullets.remove(bullet)  # Remove the bullet when it goes off-screen

        # Check for collisions with invaders
        for invader in invaders[:]:
            if bullet.rect.colliderect(invader.rect):
                invaders.remove(invader)  # Remove the invader
                bullets.remove(bullet)  # Remove the bullet
                break  # Exit the loop after a collision

    # Check for collisions between invaders and player
    for invader in invaders:
        if player.rect.colliderect(invader.rect):
            game_over = True  # End the game if player collides with invader

    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Exit cleanly
sys.exit(0)
