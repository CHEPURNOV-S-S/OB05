# /ui_components/log_display.py

from typing import List, Tuple
import pygame
from .base import UIComponent
from rpg_game.game.events import Events
import weakref


class LogDisplay(UIComponent):
    _instances = set()

    def __init__(self,
                 relative_pos: Tuple[int, int],
                 max_messages=5):
        super().__init__()
        print(f"[LOG] Created instance: {id(self)}")
        self.messages: List[str] = []
        self.max_messages = max_messages
        self.font = pygame.font.SysFont("Arial", 16)
        self.text_color = (255, 255, 255)
        self.relative_pos = relative_pos
        self.is_subscribed = False
        # Подписываемся на события при создании компонента
        self._subscribe()

    def _subscribe(self):
        if not self.is_subscribed:
            Events.LOG_MESSAGE.subscribe(self.add_message)
            self.is_subscribed = True

    def _unsubscribe(self):
        if self.is_subscribed:
            Events.LOG_MESSAGE.unsubscribe(self.add_message)
            self.is_subscribed = False

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
        if self in self._instances:
            self._instances.remove(self)
        print(f"[LOG] Destroying instance: {id(self)}")
        Events.LOG_MESSAGE.unsubscribe(self.add_message)
        self._unsubscribe()