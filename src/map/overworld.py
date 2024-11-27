from Pygame.src.setUp.settings import *
from Pygame.src.Sprite.sprites import Sprite

class Overworld:
    def __init__(self, tmx_map, data, overworld_frames):
        self.display_surface = pygame.display.get_surface()
        self.data = data

        # groups
        self.all_sprites = pygame.sprite.Group()

        self.setup(tmx_map, overworld_frames)

    def setup(self, tmx_map, overworld_frames):
        #tiles
        for layer in ['main', 'top']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, Z_LAYER['bg tiles'])

    def run(self, dt):
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)
