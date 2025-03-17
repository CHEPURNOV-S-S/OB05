#weapon/bow.py

from random import randint
from rpg_game.entities.base import Entity
from rpg_game.weapons.base import Weapon
from rpg_game.game.events import Events
from rpg_game.my_logging import Logger

class Bow(Weapon):
    def is_valid_attack(self, attacker: Entity, target: Entity) -> bool:
        distance = attacker.position.distance_to(target.position)
        return 2 <= distance <= 10

    def execute_attack(self, attacker: Entity, target: Entity) -> bool:
        distance = attacker.position.distance_to(target.position)
        chance = max(0, 100 - (distance - 2) * 10)
        if target.is_alive():
            if randint(1, 100) <= chance:
                damage = randint(10, 20)
                Logger().debug(f"Лук попадает! {damage} урона.")
                Events.LOG_MESSAGE.fire(
                    message=f"Атака луком: попадание! {damage} урона."
                )
                target.take_damage(damage)
                return True
            Logger().info("Промах!")
            Events.LOG_MESSAGE.fire(
                message=f"Атака луком: промах!"
            )
        else:
            Events.LOG_MESSAGE.fire(
                message=f"Цель уже мертва!"
            )
        return False

    def name(self) -> str:
        return 'bow'