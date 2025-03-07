# pygame_frontend/renderer.py
import pygame
from rpg_game.game.constants import MAP_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from rpg_game.game.renderer_interface import RendererInterface
from rpg_game.entities import DrawableEntity
from .asset_manager import AssetManager

class PygameRenderer(RendererInterface):
    TILE_SIZE = SCREEN_WIDTH // MAP_SIZE  # Размер одной клетки

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()
        self.assets = AssetManager()
        self.tile_size = SCREEN_WIDTH // MAP_SIZE

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
                tile = self.assets.get_sprite("tiles/grass.png")
                self.screen.blit(tile, (x * self.tile_size, y * self.tile_size))

    def _draw_entities(self, entities: list):
        for entity in entities:
            info = entity.get_render_info()
            sprite = self.assets.get_sprite(info["sprite_name"])
            pos = self._pos_to_screen(entity.position)
            # Центрируем спрайт
            pos = (pos[0] - sprite.get_width() // 2, pos[1] - sprite.get_height() // 2)
            self.screen.blit(sprite, pos)


    def _draw_status(self, fighter):
        status = f"♥{fighter.health} | ОД: {fighter.current_ap}/{fighter.max_ap}"
        text = self.font.render(status, True, (255, 255, 255))
        self.screen.blit(text, (10, SCREEN_HEIGHT - 30))

    def _pos_to_screen(self, position):
        return (position.x * self.TILE_SIZE + self.TILE_SIZE // 2,
                position.y * self.TILE_SIZE + self.TILE_SIZE // 2)