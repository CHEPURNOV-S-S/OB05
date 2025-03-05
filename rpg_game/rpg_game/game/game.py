# game/game.py
from abc import ABC, abstractmethod
from rpg_game.entities.fighter import Fighter
from rpg_game.entities.monster import Monster
from rpg_game.weapons.sword import Sword
from rpg_game.weapons.bow import Bow
from rpg_game.entities.base import Position
from .renderer_interface import RendererInterface
from .input_handler_interface import InputHandlerInterface
from .movement import MovementManager
from .constants import MAP_SIZE
import random

class Game(ABC):
    def __init__(self,
                 renderer: RendererInterface,
                 input_handler: InputHandlerInterface):
        self.renderer = renderer
        self.input_handler = input_handler
        self.fighter = Fighter(Position(5, 0), max_ap=5)
        self.monster = self._generate_monster()
        self.movement = MovementManager(MAP_SIZE)
        self._game_over = False

    def _generate_monster(self):
        while True:
            x, y = random.randint(0,9), random.randint(0,9)
            if not (x == 5 and y == 0):
                return Monster(Position(x, y))

    def run(self):
        while not self._game_over:
            self._process_game_loop()
            self._check_game_over()

    def _process_game_loop(self):
        self._player_turn()
        self._monster_turn()
        self.renderer.render(self)

    def _player_turn(self):
        while self.fighter.current_ap > 0 and not self._game_over:
            self.renderer.render(self)
            command = self.input_handler.handle_input()
            if command == 'quit':
                self._game_over = True
                return
            self._execute_command(command)
        self.fighter.reset_ap()

    def _execute_command(self, command):
        if command in ['move_n', 'move_s', 'move_e', 'move_w']:
            self._handle_movement(command)
        elif command == 'attack':
            self._handle_attack()
        elif command == 'change_weapon':
            self._handle_weapon_change()

    def _handle_movement(self, direction):
        if self.movement.move_entity(self.fighter, direction):
            self.fighter.current_ap -= 1

    def _handle_attack(self):
        if self.fighter.attack(self.monster):
            self.fighter.current_ap -= 1

    def _handle_weapon_change(self):
        # Создаём список доступных типов оружия
        weapon_classes = [Sword, Bow]

        # Определяем текущий тип оружия
        current_weapon_class = type(self.fighter.weapon) if self.fighter.weapon else None
        # Находим индекс текущего типа оружия
        current_index = weapon_classes.index(current_weapon_class) if current_weapon_class in weapon_classes else 0
        # Переключаемся на следующий тип
        new_index = (current_index + 1) % len(weapon_classes)
        new_weapon = weapon_classes[new_index]()  # Создаём новый экземпляр
        if self.fighter.change_weapon(new_weapon):
            print(f"Оружие изменено на {type(new_weapon).__name__}")


    def _monster_turn(self):
        if self.movement.move_monster_towards_target(self.monster, self.fighter):
            pass  # Monster moved
        else:
            self.monster.attack(self.fighter)

    def _check_game_over(self):
        if not self.fighter.is_alive() or not self.monster.is_alive():
            self._game_over = True