import pygame


pygame.init()


running = True

clock = pygame.time.Clock()
Fps = 60

scrn = pygame.display.set_mode([500,500])

scrn_w = scrn.get_width()
scrn_h = scrn.get_height()


class Player:
    def __init__(self, png, l, h, x, y, hp, speed):
        self.png = png
        self.l = l
        self.h = h
        self.x = x
        self.y = y
        self.hp = hp
        self.speed = speed

class Invaders:
    def __init__(self,png,l,h,s_x,s_y,speed,score):
        self.png = png
        self.l = l
        self.h = h
        self.s_x = s_x
        self.s_y = s_y
        self.speed = speed
        self.score = score




player = Player(pygame.image.load("defender.png").convert(),35,30,(scrn_w/2),(scrn_h-50),100,3)
player.png = pygame.transform.scale(player.png, (player.l, player.h))

invader1 = Invaders(pygame.image.load("invader1.png").convert(),35,30,(scrn_w+20),(scrn_h+20),1,50)
invaders1 = []


while running is True:
    event = pygame.event.wait ()
    if event.type == pygame.QUIT:
        running = False

    keys = pygame.key.get_pressed()
    pygame.key.set_repeat(2)
    if keys[pygame.K_LEFT] and player.x>0:
        player.x -= player.speed
    if keys[pygame.K_RIGHT] and player.x <= scrn_w - player.png.get_width():
        player.x += player.speed


    


    scrn.fill("black")
    scrn.blit(player.png,(player.x,player.y))
    clock.tick(Fps)
    pygame.display.update()


pygame.quit ()