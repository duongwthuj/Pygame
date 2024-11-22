import pygame.sprite

from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf=pygame.Surface((TILE_SIZE, TILE_SIZE)), groups=None):
        super().__init__(groups)
        self.image = surf
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()
