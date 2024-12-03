#%reset - f
import pygame
import sys

pygame.init()


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

class Bullet:
    def __init__(self, x, y, w, h, s):
        self.x = x
        self.y = y
        #self.img = img
        self.width = w
        self.height = h
        #self.img = pygame.transform.scale(img, (w, h))
        self.speed = s
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #pygame.Rect()

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class Octopus(Invader):
    def __init__(self, x, y, img, l, h):
        super().__init__(x, y, img, l, h, 10) #10 points for Octopus

class Crab(Invader):
    def __init__(self, x, y, img, l, h):
        super().__init__(x, y, img, l, h, 20) #20 points for Crab

class Squid(Invader):
    def __init__(self, x, y, img, l, h):
        super().__init__(x, y, img, l, h, 30) #30 points for Squid

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600

screen = pygame.display.set_mode([SCREEN_HEIGHT, SCREEN_WIDTH])

clock = pygame.time.Clock()  # to slow down the speed of movement
FPS = 60  # to slow down the speed of movement

player = Player((SCREEN_WIDTH / 2) - (35 / 2), (SCREEN_HEIGHT - 100), pygame.image.load("defender.png"), 35, 30)

# player_x = 250
# player_img = pygame.image.load("defender.png") #load in the image

invader_startrow = 100
invader_endrow = 300
invader_startcol = 100
invader_endcol = 400

moveRight = True


# Using OOP rather than variables below
# Invader((invaders_x_left + (j * 30) + 30), current_row, pygame.image.load("img/invader1.png"), 30, 30)

# invader_img = pygame.image.load("invader1.png")
# invader_img = pygame.transform.scale(invader_img, (30, 30))

# player_img = pygame.transform.scale(player_img, (35, 30)) # change the scale


def draw_invaders():
    for row in range(invader_startrow, invader_endrow, 30):  # intervals of 30
        for col in range(invader_startcol, invader_endcol, 30):
            # screen.blit(invader_img, (col, row))
            inv_obj = Invader(col, row, pygame.image.load("invader1.png"), 30, 30)
            screen.blit(inv_obj.img, (col, row))


def move_invaders():
    global invader_startcol, invader_endcol, invader_startrow, invader_endrow, moveRight
    # start moving right
    if moveRight == True:
        invader_startcol += 4
        invader_endcol += 4
        edge_hit = False
    else:  # otherwise move left
        invader_startcol -= 4
        invader_endcol -= 4
        edge_hit = False

    # detect edge of screen
    if invader_endcol > SCREEN_WIDTH or invader_startcol < 0:
        edge_hit = True
        invader_startrow += 20
        invader_endrow += 20

    # immediately reset edge_hit to prevent getting stuck!
    if edge_hit == True:
        edge_hit == False
        if moveRight == True:
            moveRight = False
        else:
            moveRight = True


running = True
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
            elif event.key == pygame.K_ESCAPE or event.key == pygame.WINDOWCLOSE:  # TO QUIT
                running = False
                # pygame.display.quit()
                # pygame.QUIT()
                # sys.exit()

    screen.fill([0, 0, 0])  # black background

    move_invaders()

    draw_invaders()

    # screen.blit(player_img, (player_x, 450)) # draw player
    screen.blit(player.img, (player.x, player.y))  # using player objects x and y and img attribute

    pygame.display.flip()

    clock.tick(FPS)

# pygame.display.quit()
# pygame.quit()
sys.exit(0)