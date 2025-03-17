# game/game.py
from abc import ABC, abstractmethod
from rpg_game.entities import DrawableEntity, Fighter, Monster, Position
from rpg_game.weapons.sword import Sword
from rpg_game.weapons.bow import Bow
from rpg_game.game.events import Events
from rpg_game.my_logging import Logger

from .renderer_interface import RendererInterface
from .input_handler_interface import InputHandlerInterface
from .movement import MovementManager
from .constants import MAP_WIDTH, MAP_HEIGHT
from .map import GameMap

import random



class Game(ABC):
    def __init__(self,
                 renderer: RendererInterface,
                 input_handler: InputHandlerInterface):
        self.renderer = renderer
        self.input_handler = input_handler

        self.game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
        self._generate_map()

        self.fighter = Fighter(Position(5, 0), max_ap=5)
        self.monster = self._generate_monster()

        self.game_map.set_player(self.fighter)

        self.movement = MovementManager(self.game_map)
        self._game_over = False
        self._game_result = None
        Events.ENTITY_DIED.subscribe(self._handle_entity_death)  # Подписка на смерть сущностей
        self._print_controls()

    def _generate_monster(self):
        while True:
            map_width, map_height = self.game_map.get_size()
            x, y = random.randint(0,map_width-1), random.randint(0,map_height-1)
            if self.game_map.is_passable(Position(x, y)):
                if not (x == 5 and y == 0):
                    return Monster(Position(x, y))

    def _generate_map(self):
        # Пример генерации
        width, height = self.game_map.get_size()
        for y in range(height):
            for x in range(width):
                if x == 5 and y == 0:
                    continue
                if random.random() < 0.1:
                    self.game_map.init_tile(x, y, 'grass', 'objects', ['rock'])
                    Logger().debug (f'скала на {x}, {y}')
                elif random.random() < 0.1:
                    self.game_map.init_tile(x, y, 'grass', 'objects', ['tree'])
                    Logger().debug (f'дерево на {x}, {y}')

    def run(self):
        while not self._game_over:
            self._process_game_loop()
            self._check_game_over()

        while self._game_result :
            command = self.input_handler.handle_input()
            if command in ['quit', 'exit' ]:
                break

    def get_entities(self) -> list[DrawableEntity]:
        return [self.fighter, self.monster]

    def _process_game_loop(self):
        self._player_turn()
        self._monster_turn()
        self.renderer.render(self.game_map)

    def _player_turn(self):
        while self.fighter.current_ap > 0 and not self._game_over:
            self.renderer.render(self.game_map)
            command = self.input_handler.handle_input()
            if command in ['quit', 'exit' ]:
                self._game_over = True
                return
            if command == 'end_turn':
                break
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
        self.fighter.attack(self.monster)

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

            Logger().info(f"Оружие изменено на {type(new_weapon).__name__}")
            Events.LOG_MESSAGE.fire(message=f"Оружие изменено на {type(new_weapon).__name__}")

    def _handle_entity_death(self, entity):
        """Обработка смерти сущностей"""
        if entity == self.fighter:
            self._game_over = True
            self._game_result = "Вы проиграли!"
        elif entity == self.monster:
            self._game_over = True
            self._game_result = "Вы выиграли!"

        Events.LOG_MESSAGE.fire(message=f"{self._game_result}")
        Events.LOG_MESSAGE.fire(message=f'Для выхода нажмите "Escape"')

    def _print_controls(self):
        Events.LOG_MESSAGE.fire(message=f'------------------------------')
        Events.LOG_MESSAGE.fire(message=f'Escape - Выход')
        Events.LOG_MESSAGE.fire(message=f'Enter - Завершить ход')
        Events.LOG_MESSAGE.fire(message=f'Space - Атака')
        Events.LOG_MESSAGE.fire(message=f'С - сменить оружие')
        Events.LOG_MESSAGE.fire(message=f'Двигаться: ↑ ↓ ← →')
        Events.LOG_MESSAGE.fire(message=f'=== Управление ===')

    def _monster_turn(self):
        if self.monster.is_alive():
            if self.movement.move_monster_towards_target(self.monster, self.fighter):
                pass  # Monster moved
            else:
                self.monster.attack(self.fighter)

    def _check_game_over(self):
        if not self.fighter.is_alive() or not self.monster.is_alive():
            self._game_over = True