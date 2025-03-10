#game/renderer_interface.py

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rpg_game.game import IGameMap

class RendererInterface(ABC):
    def __init__(self):
        self.status_panel = None
    @abstractmethod
    def render(self, game_map: "IGameMap") -> None:
        pass