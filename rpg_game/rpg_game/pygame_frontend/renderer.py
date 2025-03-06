# pygame_frontend/renderer.py
import pygame
from rpg_game.game.constants import MAP_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from rpg_game.game.renderer_interface import RendererInterface
from rpg_game.entities import DrawableEntity

class PygameRenderer(RendererInterface):
    TILE_SIZE = SCREEN_WIDTH // MAP_SIZE  # Размер одной клетки

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()

    def render(self, game):
        self.screen.fill((30, 30, 30))  # Темный фон
        self._draw_grid()
        entities = game.get_entities()
        self._draw_entities(entities)
        self._draw_status(game.fighter)
        pygame.display.flip()
        self.clock.tick(60)


    def _draw_grid(self):
        for x in range(MAP_SIZE):
            for y in range(MAP_SIZE):
                rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE,
                                   self.TILE_SIZE, self.TILE_SIZE)
                pygame.draw.rect(self.screen, (60, 60, 60), rect, 1)

    def _draw_entities(self, entities: list[DrawableEntity]):
        for entity in entities:
            info = entity.get_render_info()
            pygame.draw.circle(
                self.screen,
                info["color"],
                self._pos_to_screen(entity.position),
                info["radius"]
            )

    def _draw_status(self, fighter):
        status = f"♥{fighter.health} | ОД: {fighter.current_ap}/{fighter.max_ap}"
        text = self.font.render(status, True, (255, 255, 255))
        self.screen.blit(text, (10, SCREEN_HEIGHT - 30))

    def _pos_to_screen(self, position):
        return (position.x * self.TILE_SIZE + self.TILE_SIZE // 2,
                position.y * self.TILE_SIZE + self.TILE_SIZE // 2)