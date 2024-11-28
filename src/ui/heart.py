from Pygame.src.Sprite.animatedSprite import AnimatedSprite
from random import randint
from Pygame.src.setUp.settings import *

class Heart(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.active = False

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.active = False
            self.frame_index = 0

    def update(self, dt):
        if self.active:
            self.animate(dt)
        else:
            if randint(0, 1000) == 1: # chance of heart animation
                self.active = True
                self.frame_index = 0