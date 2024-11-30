from Pygame.src.Sprite.sprites import Sprite
from Pygame.src.setUp.settings import *


class PathSprite(Sprite):
    def __init__(self, pos, surf, groups, level):
        super().__init__(pos, surf, groups, Z_LAYER['path'])
        self.level = level
