from setUp.settings import *
from showmenu import show
import pygame
import sys

class showMenuPause:
    def __init__(self):
        self.showMenuBack = show()
        self.display_surface = pygame.display.get_surface()
        self.paused = False
        self.overworldback = False

    def show_pause_menu(self):
        # Create a surface for the pause menu
        pause_menu_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        pause_menu_surface.set_alpha(128)  # Semi-transparent
        pause_menu_surface.fill('BLACK')

        # Create menu text using Pygame font rendering
        font = pygame.font.Font(None, 36)  # Use a font (None means the default)
        resume_text = font.render('Press R to resume', True, (255, 255, 255))
        quit_text = font.render('Press Q to quit', True, (255, 255, 255))
        overworld_text = font.render('Press O to go to overworld', True, (255, 255, 255))

        # Positions for the text
        resume_rect = resume_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, 2 * WINDOW_HEIGHT // 3))
        overworld_rect = overworld_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        # Draw the menu background and text
        self.display_surface.blit(pause_menu_surface, (0, 0))  # Blit semi-transparent surface
        self.display_surface.blit(resume_text, resume_rect)
        self.display_surface.blit(quit_text, quit_rect)
        self.display_surface.blit(overworld_text, overworld_rect)

        pygame.display.update()

        # Menu event loop
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.resume_game()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_o:
                        self.overworldback = True
                        self.paused = False

    def get_overworldback(self):
        return self.overworldback

    def resume_game(self):
        # Resume the game and go back to the current level
        self.paused = False

    def pause_game(self):
        self.paused = True
        self.show_pause_menu()