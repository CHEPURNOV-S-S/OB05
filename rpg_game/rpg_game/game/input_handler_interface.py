# game/input_handler_interface.py

from abc import ABC, abstractmethod

class InputHandlerInterface(ABC):
    @abstractmethod
    def handle_input(self) -> str:
        pass