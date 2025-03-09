# entities/base.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from rpg_game.game.events import Events

@dataclass
class Position():
    x: int
    y: int

    def distance_to(self, other: 'Position') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def is_at(self, x: int, y: int) -> bool:
        return self.x == x and self.y == y

    def is_adjacent_to(self, other: 'Position') -> bool:
        return self.distance_to(other) == 1



class Entity(ABC):
    def __init__(self, position: Position, health: int):
        self._position = position
        self.health = health
        Events.ENTITY_CREATED.fire(entity=self)  # Уведомление о создании


    def take_damage(self, damage: int):
        self.health = max(self.health - damage, 0)
        if self.health <=  0:
            self._die()
        return self.health <= 0

    def _die(self):

        print(f"{type(self).__name__} умер" )
        Events.LOG_MESSAGE.fire(
            message=f"{type(self).__name__} умер"
        )
        Events.ENTITY_DIED.fire(entity=self)  # Уведомление о смерти

    def is_alive(self) -> bool:
        return self.health > 0

    def calculate_distance(self, other: 'Entity') -> int:
       return self.position.distance_to(other.position)

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, new_pos: Position):
        # Только простая проверка типа
        if not isinstance(new_pos, Position):
            raise TypeError("Ожидался Position")
        if new_pos != self._position:
            old_pos = self._position
            self._position = new_pos
            Events.ENTITY_MOVED.fire(  # Уведомление о перемещении
                entity=self,
                old_pos=old_pos,
                new_pos=new_pos
            )
            Events.LOG_MESSAGE.fire(
                message=f"{type(self).__name__} переместился на ({new_pos.x}, {new_pos.y})"
            )

    def _on_position_change(self, new_pos: Position):
        print(f"{type(self).__name__} moved to {new_pos}")


class DrawableEntity(Entity):
    @abstractmethod
    def get_render_info(self) -> dict:
        """Возвращает данные для отрисовки: цвет, спрайт и т.д."""
        pass