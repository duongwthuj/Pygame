from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Platformer")

        self.tmx_maps = {0: load_pygame(join('..', 'data', 'levels', 'omni.tmx'))}

        self.current_state = Level(self.tmx_maps[0])

        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.current_state.run(0.1)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
