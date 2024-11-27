from math import radians
from tarfile import data_filter

from Pygame.src.Sprite.movingSprite import MovingSprite
from Pygame.src.setUp.settings import *
from Pygame.src.Sprite.sprites import Sprite
from Pygame.src.objPlay.player import Player
from Pygame.src.Sprite.groups import AllSprites
from Pygame.src.Sprite.animatedSprite import AnimatedSprite
from Pygame.src.Sprite.spike import Spike

class Level:
    def __init__(self, tmx_map, level_frames):
        self.display_surface = pygame.display.get_surface()


        #level data
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_bottom = tmx_map.width * TILE_SIZE
        tmx_level_properties = tmx_map.get_layer_by_name('Data')[0].properties
        if tmx_level_properties['bg']:
            bg_tile = level_frames['bg_tiles'][tmx_level_properties['bg']]
        else:
            bg_tile = None

        #groups
        self.all_sprites = AllSprites(
            width = tmx_map.width,
            height = tmx_map.height,
            bg_tile = bg_tile,
            top_limit = tmx_level_properties['top_limit'],
            clouds = {'large': level_frames['cloud_large'], 'small': level_frames['cloud_small']},
            horizon_line = tmx_level_properties['horizon_line']
        )
        self.collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.sem_collision_sprites = pygame.sprite.Group()  # collision sprites other
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
                        z = Z_LAYER['fg']
                    case _:
                        z = Z_LAYER['main']

                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, z)

        # objects
        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == "player":
                self.player = Player(
                    pos = (obj.x, obj.y),
                    groups = self.all_sprites,
                    collision_sprites= self.collision_sprites,
                    sem_collision_sprites=self.sem_collision_sprites,
                    frames = level_frames['player'])
            else:
                if obj.name in ('barrel', 'crate'):
                    Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
                else:
                    if 'palm' not in obj.name:
                        frames = level_frames[obj.name]
                        if obj.name == 'floor_spike' and obj.properties['inverted']:
                            frames = [pygame.transform.flip(frame, False, True) for frame in frames]
                        AnimatedSprite((obj.x, obj.y), frames, (self.all_sprites))

                    else:
                        frames = level_frames['palms'][obj.name]
                        z = Z_LAYER['main'] if not 'bg' in obj.name else Z_LAYER['bg details']
                        AnimatedSprite((obj.x, obj.y), frames, (self.all_sprites), z)
            #level finish
            if obj.name == 'flag':
                self.level_finish_rect = pygame.FRect((obj.x, obj.y), (obj.width, obj.height))

        # bg details
        for obj in tmx_map.get_layer_by_name("BG details"):
            if obj.name == 'static':
                Sprite((obj.x, obj.y), obj.image, (self.all_sprites), Z_LAYER['bg tiles'])
            else:
                frames = level_frames[obj.name]
                AnimatedSprite((obj.x, obj.y), frames, (self.all_sprites), Z_LAYER['bg details'])
                if obj.name == 'candle':
                    AnimatedSprite((obj.x, obj.y) + vector(-20, -20), level_frames['candle_light'], self.all_sprites, Z_LAYER['bg details'])

        # moving obj
        for obj in tmx_map.get_layer_by_name("Moving Objects"):
            if obj.name == 'spike':
                Spike(
                    pos=(obj.x + obj.width/2, obj.y + obj.height/2), # top left corner -> center
                    surf =level_frames['spike'],
                    radius = obj.properties['radius'],
                    speed = obj.properties['speed'],
                    start_angle = obj.properties['start_angle'],
                    end_angle = obj.properties['end_angle'],
                    groups = (self.all_sprites, self.damage_sprites)
                )
                for radius in range(0, obj.properties['radius'], 20):
                    Spike(
                        pos=(obj.x + obj.width/2, obj.y + obj.height/2), # top left corner -> center
                        surf =level_frames['spike_chain'],
                        radius = radius,
                        speed = obj.properties['speed'],
                        start_angle = obj.properties['start_angle'],
                        end_angle = obj.properties['end_angle'],
                        groups = (self.all_sprites),
                        z = Z_LAYER['bg details']
                    )
            else:
                frames = level_frames[obj.name]
                groups =(self.all_sprites, self.collision_sprites) if obj.properties['platform'] else (self.all_sprites, self.damage_sprites)
                if obj.width > obj.height:  # horizontal
                    move_dir = 'x'
                    start_pos = (obj.x, obj.y + obj.height / 2)
                    end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
                else:  # vertical
                    move_dir = 'y'
                    start_pos = (obj.x + obj.width / 2, obj.y)
                    end_pos = (obj.x + obj.width / 2, obj.y + obj.height)
                speed = obj.properties['speed'] / 2
                MovingSprite(frames, groups, start_pos, end_pos, move_dir, speed, obj.properties['flip'])

                if obj.name == 'saw':
                    if move_dir == 'x':
                        y = start_pos[1] - level_frames['saw_chain'].get_height() /2
                        left, right = int(start_pos[0]), int(end_pos[0])
                        for x in range(left, right, 20):
                            Sprite((x, y), level_frames['saw_chain'], self.all_sprites, Z_LAYER['bg details'])
                    else:
                        x = start_pos[0] - level_frames['saw_chain'].get_width() / 2
                        top, bottom = int(start_pos[1]), int(end_pos[1])
                        for y in range(top, bottom, 20):
                            Sprite((x, y), level_frames['saw_chain'], self.all_sprites, Z_LAYER['bg details'])

        #water
        for obj in tmx_map.get_layer_by_name("Water"):
            rows = int(obj.height / TILE_SIZE)
            cols = int(obj.width / TILE_SIZE)
            for row in range(rows):
                for col in range(cols):
                    x = obj.x + col * TILE_SIZE
                    y = obj.y + row * TILE_SIZE
                    if row == 0:
                        AnimatedSprite((x, y), level_frames['water_top'], (self.all_sprites), Z_LAYER['water'])
                    else:
                        Sprite((x, y), level_frames['water_body'], (self.all_sprites), Z_LAYER['water'])

    def check_constraint(self):  # check if player is out of screen
        #left right
        if self.player.hitbox_rect.left <= 0:
            self.player.hitbox_rect.left = 0
        if self.player.hitbox_rect.right >= self.level_width:
            self.player.hitbox_rect.right = self.level_width

        #bottom
        if self.player.hitbox_rect.bottom > self.level_bottom:
            pass

        #success
        if self.player.hitbox_rect.colliderect(self.level_finish_rect):
            print('success')

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.player.hitbox_rect.center, dt)
        self.check_constraint()
