# ui_components/health_display.py

import pygame

from typing import Tuple
from pygame.cursors import sizer_x_strings

from .base import UIComponent
from ..asset_manager import AssetManager


class HealthDisplay(UIComponent):
    def __init__(self, asset_manager: AssetManager,
                 relative_pos: Tuple[int, int]):
        super().__init__()
        self.asset_manager = asset_manager
        self.health = 100
        self.max_health = 50
        self.relative_pos = relative_pos

    def render(self, screen: pygame.Surface,
               pos: Tuple[int,int]):
        # Текст
        font = pygame.font.SysFont("Arial", 25)
        text = font.render(f"ОЗ: {self.health:3}/{self.max_health:3}", True, (255, 255, 255))

        pos = (pos[0]+self.relative_pos[0], pos[1]+self.relative_pos[1])
        size = (100, 64)
        rect = pygame.Rect(pos, size)
        screen.blit(text, rect.topleft)

        # Спрайты сердец
        heart = self.asset_manager.get_sprite("ui/heart.png")
        empty_heart = self.asset_manager.get_sprite("ui/heart_empty.png")
        for i in range(self.max_health // 20):
            x = rect.x + 120 + i * 30
            sprite = heart if i < self.health // 20 else empty_heart
            screen.blit(sprite, (x, rect.y))

    def update(self, data: dict):
        self.health = data.get('health', 0)
        self.max_health = data.get('max_health', 100)