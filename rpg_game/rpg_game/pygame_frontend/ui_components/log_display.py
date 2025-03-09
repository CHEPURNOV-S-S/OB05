# pygame_frontend/ui_components/log_display.py

from typing import List, Tuple
import pygame
from .base import UIComponent
from rpg_game.game.events import Events
import weakref


class LogDisplay(UIComponent):
    _instances = weakref.WeakSet()  # Для отслеживания всех экземпляров

    def __init__(self,
                 relative_pos: Tuple[int, int],
                 max_messages=5):
        super().__init__()
        print("[LOG] Creating LogDisplay")  # Отладка
        self.messages: List[str] = []
        self.max_messages = max_messages
        self.font = pygame.font.SysFont("Arial", 16)
        self.text_color = (255, 255, 255)
        self.relative_pos = relative_pos

        # Подписываемся на события при создании компонента
        Events.LOG_MESSAGE.subscribe(self.add_message)

    def update(self, data: dict):
        pass

    def add_message(self, **kwargs):
        message = ''
        if 'message' in kwargs:
            message = kwargs['message']

        self.messages.append(message)
        print(f"Сообщение получено: {message}")
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def render(self, screen: pygame.Surface, pos: tuple):
        y_offset = self.relative_pos[1]+pos[1]
        for message in reversed(self.messages):
            text_surf = self.font.render(message, True, self.text_color)
            screen.blit(text_surf, (self.relative_pos[0]+pos[0], y_offset))
            y_offset += text_surf.get_height() + 2

    def __del__(self):
        print("[LOG] Destroying LogDisplay")  # Отладка
        Events.LOG_MESSAGE.unsubscribe(self.add_message)