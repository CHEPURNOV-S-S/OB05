from abc import ABC, abstractmethod
from typing import Tuple
import pygame

class UIComponent(ABC):
    def __init__(self):
        self.visible = True

    @abstractmethod
    def render(self,
               screen: pygame.Surface,
               pos: Tuple[int, int]):
        pass

    @abstractmethod
    def update(self, data: dict):
        pass

    def handle_event(self, event: pygame.event.Event):
        pass