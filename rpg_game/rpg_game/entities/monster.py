# entities/monster.py

from ..entities.base import Entity, Position, DrawableEntity
from ..weapons.base import Weapon
import random

class Monster(DrawableEntity):
    def __init__(self, position: Position):
        super().__init__(position, health=50)

    def take_damage(self, damage: int):
        self.health -= damage
        if self.health < 0: self.health = 0

    def attack(self, target: Entity):
        if self.calculate_distance(target) == 1:
            damage = random.randint(10, 20)
            target.take_damage(damage)
            print(f"Монстр атакует! {damage} урона.")
            return True
        return False

    def get_render_info(self) -> dict:
        return {
            "sprite_name": "monster.png",  # Только имя файла
            "size": (64, 64),  # Размер спрайта
            "offset": (0, 0)  # Смещение при отрисовки
        }