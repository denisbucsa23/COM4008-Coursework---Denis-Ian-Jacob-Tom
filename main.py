import pygame


pygame.init()
running = True



scrn = pygame.display.set_mode([500,500])

scrn_w = scrn.get_width()
scrn_h = scrn.get_height()
player_pos = pygame.Vector2(scrn_w / 2, scrn_h - 10)


player_png = pygame.image.load("defender.png")
player_png = pygame.transform.scale(player_png, (35, 30))



while running is True:
    event = pygame.event.wait ()
    if event.type == pygame.QUIT:
        running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos.x -= 5
    if keys[pygame.K_d]:
        player_pos.x += 5
    scrn.fill("black")
    scrn.blit(player_png,player_pos)
    pygame.display.update()
    pygame.display.flip()

pygame.quit ()