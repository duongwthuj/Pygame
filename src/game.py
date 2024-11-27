import pygame.transform

from Pygame.src.setUp.settings import *
from Pygame.src.map.level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from Pygame.src.setUp.support import *
from Pygame.src.map.overworld import Overworld


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Platformer")

        self.clock = pygame.time.Clock()
        self.import_assets()

        self.tmx_maps = {0: load_pygame(join('..', 'data', 'levels', 'omni.tmx'))}
        self.tmx_overworld = load_pygame(join('..', 'data', 'overworld', 'overworld.tmx'))
        self.current_state = Level(self.tmx_maps[0], self.level_frames)
        #self.current_state = Overworld(self.tmx_overworld, self.data, self.tmx_overworld_frames)

    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('..', 'graphics', 'level', 'flag'),
            'palms': import_sub_folders('..', 'graphics', 'level', 'palms'),
            'candle': import_folder('..', 'graphics', 'level', 'candle'),
            'window': import_folder('..', 'graphics', 'level', 'window'),
            'small_chain': import_folder('..', 'graphics', 'level', 'small_chains'),
            'big_chain': import_folder('..', 'graphics', 'level', 'big_chains'),
            'candle_light': import_folder('..', 'graphics', 'level', 'candle light'),
            'helicopter': import_folder('..', 'graphics', 'level', 'helicopter'),
            'water_top': import_folder('..', 'graphics', 'level', 'water', 'top'),
            'water_body': import_image('..', 'graphics', 'level', 'water', 'body'),
            'bg_tiles': import_folder_dict('..', 'graphics', 'level', 'bg', 'tiles'),
            'cloud_small': import_folder('..', 'graphics', 'level', 'clouds', 'small'),
            'cloud_large': import_image('..', 'graphics', 'level', 'clouds', 'large_cloud'),
            'saw': import_folder('..', 'graphics', 'enemies', 'saw', 'animation'),
            'floor_spike': import_folder('..', 'graphics', 'enemies', 'floor_spikes'),
            'player': import_sub_folders('..', 'graphics', 'player'),
            'saw_chain': import_image('..', 'graphics', 'enemies', 'saw', 'saw_chain'),
            'boat': import_folder('..', 'graphics', 'objects', 'boat'),
            'spike': import_image('..', 'graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
            'spike_chain': import_image('..', 'graphics', 'enemies', 'spike_ball', 'spiked_chain'),
            'tooth': import_folder('..', 'graphics', 'enemies', 'tooth', 'run'),
            'shell': import_sub_folders('..', 'graphics', 'enemies', 'shell'),
            'pearl': import_image('..', 'graphics', 'enemies', 'bullets', 'pearl'),
            'items': import_sub_folders('..', 'graphics', 'items'),
            'particle': import_folder('..', 'graphics', 'effects', 'particle'),
        }
        self.tmx_overworld_frames = {
            'water': import_folder('..', 'graphics', 'overworld', 'water'),
            'palms': import_sub_folders('..', 'graphics', 'overworld', 'palm'),
        }

    def run(self):
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.current_state.run(0.06)
            pygame.display.update()
