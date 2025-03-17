#ui_components/ap_display.py

import pygame
from typing import Tuple
from .base import UIComponent
from ..asset_manager import AssetManager


class APDisplay(UIComponent):
    def __init__(self, asset_manager: AssetManager,
                 relative_pos: Tuple[int, int]):
        super().__init__()
        self.asset_manager = asset_manager
        self.ap = 4
        self.max_ap = 5
        self.relative_pos = relative_pos

    def render(self, screen: pygame.Surface,
               pos: Tuple[int, int]):
        font = pygame.font.SysFont("Arial", 25)
        text = font.render(f"ОД: {self.ap:2}/{self.max_ap:2}", True, (255, 255, 255))
        pos = (pos[0] + self.relative_pos[0], pos[1] + self.relative_pos[1])
        size = (100, 64)
        rect = pygame.Rect(pos, size)
        screen.blit(text, rect)

        # Иконки ОД
        ap_icon = self.asset_manager.get_sprite("ui/ap_icon.png")
        for i in range(self.max_ap):
            x = rect.x + 120 + i * 30
            if i < self.ap:
                screen.blit(ap_icon, (x, rect.y))

    def update(self, data: dict):
        self.ap = data.get('current_ap', 0)
        self.max_ap = data.get('max_ap', 5)