from movingSprite import MovingSprite
from settings import *
from sprites import Sprite
from player import Player
from groups import AllSprites
from animatedSprite import AnimatedSprite


class Level:
    def __init__(self, tmx_map, level_frames):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.sem_collision_sprites = pygame.sprite.Group()  # collison sprites other
        self.setup(tmx_map, level_frames)

    def setup(self, tmx_map, level_frames):
        # tiles
        for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Terrain':
                    groups.append(self.collision_sprites)
                if layer == 'Platforms':
                    groups.append(self.sem_collision_sprites)
                z = Z_LAYER['bg tiles']
                match layer:
                    case 'BG':
                        z = Z_LAYER['bg tiles']
                    case 'FG':
                        z = Z_LAYER['bg tiles']
                    case _:
                        z = Z_LAYER['main']

                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups)

        # objects
        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == "player":
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites,
                                     self.sem_collision_sprites)
            else:
                if obj.name in ('barrel', 'crate'):
                    Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
                else:
                    if 'palm' not in obj.name:
                        frames = level_frames[obj.name]
                        AnimatedSprite((obj.x, obj.y), frames, (self.all_sprites))
        # moving obj
        for obj in tmx_map.get_layer_by_name("Moving Objects"):
            if obj.name == 'helicopter':
                if obj.width > obj.height:  # horizontal
                    move_dir = 'x'
                    start_pos = (obj.x, obj.y + obj.height / 2)
                    end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
                else:  # vertical
                    move_dir = 'y'
                    start_pos = (obj.x + obj.width / 2, obj.y)
                    end_pos = (obj.x + obj.width / 2, obj.y + obj.height)
                speed = obj.properties['speed'] / 2
                MovingSprite((self.all_sprites, self.sem_collision_sprites), start_pos, end_pos, move_dir, speed)

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.player.hitbox_rect.center)
