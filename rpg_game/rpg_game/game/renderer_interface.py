#game/renderer_interface.py

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rpg_game.game.game import Game

class RendererInterface(ABC):
    @abstractmethod
    def render(self, game: "Game") -> None:
        pass