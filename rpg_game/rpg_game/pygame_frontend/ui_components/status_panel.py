# ui_components/status_panel.py

from typing import Tuple

import pygame

from .base import UIComponent
from ..asset_manager import AssetManager
from .health_display import HealthDisplay
from .ap_display import APDisplay
from .weapon_indicator import WeaponIndicator
from .action_panel import ActionPanel
from .log_display import LogDisplay
from rpg_game.game.constants import SCREEN_WIDTH, STATUS_PANEL_HEIGHT


class StatusPanel(UIComponent):
    def __init__(self,
                 asset_manager: AssetManager):
        super().__init__( )
        self.asset_manager = asset_manager
        self.log_display = LogDisplay((500, 10), max_messages = 10) #сохраняем ссылку
        self.components = [
            HealthDisplay(self.asset_manager, (10, 10)),
            APDisplay(self.asset_manager, (10, 74)),
            WeaponIndicator(self.asset_manager, (10, 148)),
            self.log_display
           # ActionPanel(self.asset_manager)
        ]


    def render(self,
               screen: pygame.Surface,
               pos: Tuple[int, int]):
        rect = pygame.rect.Rect(pos,(SCREEN_WIDTH, STATUS_PANEL_HEIGHT))
        # Фон панели
        pygame.draw.rect(screen, (50, 50, 50), rect)

        # Отрисовка дочерних компонентов
        for component in self.components:
            component.render(screen, pos)

    def update(self, data: dict):
        for component in self.components:
            component.update(data)

    def handle_event(self, event: pygame.event.Event):
        for component in self.components:
            component.handle_event(event)