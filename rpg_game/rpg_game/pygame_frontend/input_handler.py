# pygame_frontend/input_handler.py
import pygame
from rpg_game.game.input_handler_interface import InputHandlerInterface

class PygameInputHandler(InputHandlerInterface):
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                return self._handle_key(event.key)
        return None

    def _handle_key(self, key):
        key_map = {
            pygame.K_UP: 'move_n',
            pygame.K_DOWN: 'move_s',
            pygame.K_LEFT: 'move_w',
            pygame.K_RIGHT: 'move_e',
            pygame.K_SPACE: 'attack',
            pygame.K_c: 'change_weapon'
        }
        return key_map.get(key)