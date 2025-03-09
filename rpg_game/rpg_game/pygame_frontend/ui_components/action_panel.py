import pygame

from .base import UIComponent
from ..asset_manager import AssetManager
from rpg_game.game.events import Events


class ActionPanel(UIComponent):
    def __init__(self, asset_manager: AssetManager):
        super().__init__()
        self.asset_manager = asset_manager
        self.buttons = self._create_buttons()

    def _create_buttons(self) -> list[dict]:
        return [
            {
                'size': (200, 40),
                'text': 'Сменить оружие',
                'callback': self.change_weapon
            },
            {
                'size': (200, 40),
                'text': 'Закончить ход',
                'callback': self.end_turn
            }
        ]

    def render(self, screen: pygame.Surface):
        for btn in self.buttons:
            pygame.draw.rect(screen, (100, 100, 100), btn['rect'])
            # Отрисовка текста/иконок кнопок

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.buttons:
                if btn['rect'].collidepoint(event.pos):
                    btn['callback']()

    def update(self, data: dict):
        pass

    def change_weapon(self):
        Events.WEAPON_CHANGE_REQUEST.fire()

    def end_turn(self):
        Events.END_TURN.fire()