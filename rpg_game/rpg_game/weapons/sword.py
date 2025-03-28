#weapon/sword.py

from rpg_game.weapons.base import Weapon
from rpg_game.entities.base import Entity
import random
from rpg_game.game.events import Events
from rpg_game.my_logging import Logger

class Sword(Weapon):
    def is_valid_attack(self, attacker: Entity, target: Entity) -> bool:
        distance = attacker.position.distance_to(target.position)
        return distance == 1

    def execute_attack(self, attacker: Entity, target: Entity) -> bool:
        damage = random.randint(15, 25)
        target.take_damage(damage)
        if target.is_alive():
            Logger().info(f"Меч наносит {damage} урона!")
            Events.LOG_MESSAGE.fire(
                message=f"Меч наносит {damage} урона!"
            )
            return True
        else:
            Events.LOG_MESSAGE.fire(
                message=f"Цель уже мертва!"
            )
        return False


    def name(self) -> str:
        return 'sword'
