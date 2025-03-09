# pygame_frontend/renderer.py
from typing import Tuple

import pygame
from rpg_game.game.constants import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from rpg_game.entities import DrawableEntity, Position
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
        self.draw_tiled_background(self.assets.get_terrain_sprite('grass'))
        self._draw_map(game_map)
        #self._draw_status(game.fighter)
        pygame.display.flip()
        self.clock.tick(60)

    def draw_tiled_background(self, sprite):
        sprite_width = sprite.get_width()
        sprite_height = sprite.get_height()

        for x in range(-self.tile_size//2, SCREEN_WIDTH, sprite_width):
            for y in range(-self.tile_size//2, SCREEN_HEIGHT, sprite_height):
                self.screen.blit(sprite, (x, y))

    def _draw_map(self, game_map: IGameMap):
        map_width, map_height = game_map.get_size()
        for y in range(map_height):
            for x in range(map_width):
                tile = game_map.get_tile(y,x)

                # Отрисовка всех слоёв за один проход
                self._draw_tile_layers(x, y, tile)

    def _draw_tile_layers(self, x: int, y: int, tile: Tile):
        pos_x, pos_y = self._pos_to_screen (Position(x, y))
        # 1. Слой земли
        terrain_sprite = self.assets.get_terrain_sprite(tile.layers['terrain'])
        self.screen.blit(terrain_sprite, (pos_x, pos_y))

        # 2. Слой объектов
        for obj in tile.layers['objects']:
            obj_sprite = self.assets.get_object_sprite(obj)
            if obj_sprite:
                self.screen.blit(obj_sprite, (pos_x, pos_y))

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
        # Отрисовка спрайта
        sprite = self.assets.get_sprite(info["sprite_name"])
        pos = self._pos_to_screen(entity.position)
        self.screen.blit(sprite, pos)

        # Отрисовка полосы здоровья
        health_bar = HealthBar(info)
        health_bar.draw(self.screen, pos)

    def _draw_status(self, fighter):
        status = f"♥{fighter.health} | ОД: {fighter.current_ap}/{fighter.max_ap}"
        text = self.font.render(status, True, (255, 255, 255))
        self.screen.blit(text, (10, SCREEN_HEIGHT - 30))

    def _pos_to_screen(self, position):
        return (position.x * self.tile_size + self.tile_size//2,
                position.y * self.tile_size + self.tile_size//2)

class HealthBar:
    def __init__(self,  render_info: dict):
        self.border_color = (50, 50, 50)  # Цвет рамки
        self.bg_color = (150, 0, 0)  # Цвет фона (красный)
        self.fill_color = (0, 255, 0)  # Цвет заполнения (зелёный)
        self.height = 5  # Высота полосы
        self.padding = 2  # Отступ от спрайта

        self.max_health = render_info.get('max_health', 0)
        self.current_health = render_info.get('health', 0)  # Текущее значение для анимации
        self.target_health = render_info.get('health', 0)   # Целевое значение (здоровье сущности)
        self.health_change_speed = 2  # Скорость анимации

    def draw(self, screen, entity_x_y: Tuple[int, int]):
        # Позиция над спрайтом
        x = entity_x_y[0]
        y = entity_x_y[1] - self.height - self.padding

        # Рисуем рамку
        pygame.draw.rect(screen, self.border_color,
                         (x, y, TILE_SIZE, self.height), 1)

        # Рисуем фон полосы (красный)
        pygame.draw.rect(screen, self.bg_color,
                         (x + 1, y + 1, TILE_SIZE - 2, self.height - 2))

        # Рисуем заполнение (зелёный)
        fill_width = int((self.target_health / self.max_health) * (TILE_SIZE - 2))
        pygame.draw.rect(screen, self.fill_color,
                         (x + 1, y + 1, fill_width, self.height - 2))

    # TODO: реализовать плавное изменение полосы здоровья.
    def update(self):
        # Плавное изменение
        render_info = self.entity.get_render_info()
        self.target_health = render_info.get('health', 0)  # Целевое значение (здоровье сущности)

        if self.current_health != self.target_health:
            if self.current_health < self.target_health:
                self.current_health = min(
                    self.current_health + self.health_change_speed,
                    self.target_health
                )
            else:
                self.current_health = max(
                    self.current_health - self.health_change_speed,
                    self.target_health
                )