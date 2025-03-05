# pygame_frontend/renderer.py
import pygame
from rpg_game.game.constants import MAP_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from rpg_game.game.renderer_interface import RendererInterface

class PygameRenderer(RendererInterface):
    TILE_SIZE = SCREEN_WIDTH // MAP_SIZE  # Размер одной клетки

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()

    def render(self, game):
        self.screen.fill((30, 30, 30))  # Темный фон
        self._draw_grid()
        self._draw_entities(game.fighter, game.monster)
        self._draw_status(game.fighter)
        pygame.display.flip()
        self.clock.tick(60)


    def _draw_grid(self):
        for x in range(MAP_SIZE):
            for y in range(MAP_SIZE):
                rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE,
                                   self.TILE_SIZE, self.TILE_SIZE)
                pygame.draw.rect(self.screen, (60, 60, 60), rect, 1)

    def _draw_entities(self, fighter, monster):
        # Игрок - зеленый круг
        pygame.draw.circle(self.screen, (0, 255, 0),
                           self._pos_to_screen(fighter.position),
                           self.TILE_SIZE // 3)

        # Монстр - красный круг
        pygame.draw.circle(self.screen, (255, 0, 0),
                           self._pos_to_screen(monster.position),
                           self.TILE_SIZE // 3)

    def _draw_status(self, fighter):
        status = f"♥{fighter.health} | ОД: {fighter.current_ap}/{fighter.max_ap}"
        text = self.font.render(status, True, (255, 255, 255))
        self.screen.blit(text, (10, SCREEN_HEIGHT - 30))

    def _pos_to_screen(self, position):
        return (position.x * self.TILE_SIZE + self.TILE_SIZE // 2,
                position.y * self.TILE_SIZE + self.TILE_SIZE // 2)