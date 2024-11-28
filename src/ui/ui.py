from Pygame.src.setUp.settings import *
from Pygame.src.setUp.timer import Timer
from Pygame.src.ui.heart import Heart
class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font


        #health/hearts
        self.heart_frames = frames['heart']
        self.heart_surf_width = self.heart_frames[0].get_width()
        self.heart_padding = 7

        #coins
        self.coin_amount = 0
        self.coin_timer = Timer(2000)
        self.coin_surf = frames['coin']

    def create_hearts(self, amount):
        for sprite in self.sprites:
            sprite.kill()
        for heart in range(amount):
            x = 10 + (self.heart_surf_width + self.heart_padding) * heart
            y = 10
            Heart((x,y), self.heart_frames, self.sprites)

    def display_text(self):
        if self.coin_timer.active: #only show coins for a short time
            text_surf = self.font.render(str(self.coin_amount), False, '#33323d')
            text_rect = text_surf.get_frect(topleft = (16, 32))
            self.display_surface.blit(text_surf, text_rect)

            coin_rect = self.coin_surf.get_frect(center = text_rect.bottomright).move(0, -5)
            self.display_surface.blit(self.coin_surf, coin_rect)

    def show_coins(self, amount):
        self.coin_amount = amount
        self.coin_timer.activate()

    def update(self, dt):
        self.coin_timer.update() #coin timer
        self.sprites.update(dt)
        self.sprites.draw(self.display_surface)
        self.display_text()