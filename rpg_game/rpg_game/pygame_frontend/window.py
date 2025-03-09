# pygame_frontend/window.py

import pygame
from rpg_game.game.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class PygameWindow:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('RPG Game')
        self.clock = pygame.time.Clock()

    def close(self):
        pygame.quit()