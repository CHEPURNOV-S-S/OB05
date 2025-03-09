import pygame
from typing import Tuple
from .base import UIComponent
from ..asset_manager import AssetManager


class WeaponIndicator(UIComponent):
    def __init__(self, asset_manager: AssetManager,
                 relative_pos: Tuple[int, int]):
        super().__init__()
        self.asset_manager = asset_manager
        self.weapon = 'bow'  # Значение по умолчанию
        self.weapon_ui_str = {'bow':'Лук', 'sword':'Меч'}
        self.relative_pos = relative_pos

    def render(self, screen: pygame.Surface,
               pos: Tuple[int, int]):
        pos = (pos[0] + self.relative_pos[0], pos[1] + self.relative_pos[1])
        size = (100, 64)
        rect = pygame.Rect(pos, size)
        # Название
        font = pygame.font.SysFont("Arial", 25)
        weapon_str = self.weapon_ui_str.get(self.weapon, '')
        text = font.render(f"Оружие: {weapon_str}", True, (255, 255, 255) )
        screen.blit(text, rect.topleft)

        # Иконка оружия
        if len(self.weapon) > 0:
            icon = self.asset_manager.get_sprite(f"weapons/{self.weapon}.png")
            screen.blit(icon, (pos[0] + 150, pos[1]))

    def update(self, data: dict):
        self.weapon = data.get('weapon', '')