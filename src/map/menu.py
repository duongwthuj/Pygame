from Pygame.src.setUp.settings import *
from os.path import join

class Menu:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pygame.font.Font(join('..', 'graphics', 'ui', 'runescape_uf.ttf'), 50)
        self.buttons = [
            {'text': 'Play', 'rect': pygame.Rect(WINDOW_WIDTH // 2 - 100, 200, 200, 50)},
            #{'text': 'Options', 'rect': pygame.Rect(WINDOW_WIDTH // 2 - 100, 400, 200, 50)},
            {'text': 'Quit', 'rect': pygame.Rect(WINDOW_WIDTH // 2 - 100, 300, 200, 50)},
        ]
        self.bg_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.highlight_color = (50, 50, 50)
        self.running = True
        self.selected_action = None

    def draw_buttons(self):
        for button in self.buttons:
            color = self.highlight_color if button['rect'].collidepoint(pygame.mouse.get_pos()) else self.bg_color
            pygame.draw.rect(self.display_surface, color, button['rect'])
            text_surface = self.font.render(button['text'], True, self.text_color)
            text_rect = text_surface.get_rect(center=button['rect'].center)
            self.display_surface.blit(text_surface, text_rect)

    def run(self):
        while self.running:
            self.display_surface.fill(self.bg_color)
            self.draw_buttons()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button['rect'].collidepoint(event.pos):
                            self.selected_action = button['text']
                            self.running = False
                            break