import pygame

class Sprit:
    def __init__(self,name,png,hp):
        self.name = name
        self.png = png
        self.hp = hp


class Player(Sprit):
    super(__init__)

    def player_move(self,keys,player_png):
        if keys[pygame.K_a]:
            player_png -= 5


