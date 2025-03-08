# pygame_frontend/renderer.py
import pygame
from rpg_game.game.constants import TILE_SIZE
from rpg_game.entities import DrawableEntity
from rpg_game.game import IGameMap, Tile, RendererInterface
from .asset_manager import AssetManager


class PygameRenderer(RendererInterface):

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()
        self.assets = AssetManager()
        self.tile_size = TILE_SIZE

    def render(self, game_map: IGameMap):
        self.screen.fill((30, 30, 30))  # Темный фон
        self._draw_map(game_map)
        #self._draw_status(game.fighter)
        pygame.display.flip()
        self.clock.tick(60)

    def _draw_map(self, game_map: IGameMap):
        map_width, map_height = game_map.get_size()
        for y in range(map_height):
            for x in range(map_width):
                tile = game_map.get_tile(y,x)

                # Отрисовка всех слоёв за один проход
                self._draw_tile_layers(x, y, tile)

    def _draw_tile_layers(self, x: int, y: int, tile: Tile):
        # 1. Слой земли
        terrain_sprite = self.assets.get_terrain_sprite(tile.layers['terrain'])
        self.screen.blit(terrain_sprite, (x * self.tile_size, y * self.tile_size))

        # 2. Слой объектов
        for obj in tile.layers['objects']:
            obj_sprite = self.assets.get_object_sprite(obj)
            if obj_sprite:
                self.screen.blit(obj_sprite, (x * self.tile_size, y * self.tile_size))

        # 3. Слой сущностей (с учётом z-порядка)
        for entity in tile.layers['entities']:
            self._draw_entity(entity)

        # 4. Слой эффектов
        """for effect in tile.layers['effects']:
            effect_sprite = self.assets.get_effect_sprite(effect)
            if effect_sprite:
                self.screen.blit(effect_sprite, (x * self.tile_size, y * self.tile_size))"""

    def _draw_entity(self, entity: DrawableEntity):
        info = entity.get_render_info()
        sprite = self.assets.get_sprite(info["sprite_name"])
        pos = self._pos_to_screen(entity.position)
        self.screen.blit(sprite, pos)

    def _draw_status(self, fighter):
        status = f"♥{fighter.health} | ОД: {fighter.current_ap}/{fighter.max_ap}"
        text = self.font.render(status, True, (255, 255, 255))
        self.screen.blit(text, (10, SCREEN_HEIGHT - 30))

    def _pos_to_screen(self, position):
        return (position.x * self.tile_size,
                position.y * self.tile_size)