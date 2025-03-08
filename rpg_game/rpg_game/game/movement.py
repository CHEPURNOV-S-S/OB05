# game/movement.py
from rpg_game.entities.base import Entity
from rpg_game.entities.fighter import Fighter
from rpg_game.entities.monster import Monster
from rpg_game.entities.base import Position
from .map import GameMap

class MovementManager:
    def __init__(self, game_map: GameMap):
        self.game_map = game_map

    def move_entity(self, entity: Entity, direction: str) -> bool:
        """Перемещение игрока по направлению"""
        new_x, new_y = entity.position.x, entity.position.y
        if direction == 'move_n': new_y -= 1
        elif direction == 'move_s': new_y += 1
        elif direction == 'move_e': new_x += 1
        elif direction == 'move_w': new_x -= 1
        else: return False

        if self.game_map.is_passable(Position(new_x, new_y)):
            old_x, old_y = entity.position.x, entity.position.y
            self.game_map.set_tile_layer(old_x, old_y, 'entities', None)
            entity.position = Position(new_x, new_y)
            self.game_map.set_tile_layer(new_x, new_y, 'entities', [entity])
            return True
        return False

    def move_monster_towards_target(self, monster: Monster, target: Entity) -> bool:
        """ИИ-перемещение монстра на 1 шаг ближе к цели, но не ближе чем на расстояние 1"""
        current_distance = monster.position.distance_to(target.position)

        # Если монстр уже рядом (расстояние <= 1), не двигаемся
        if current_distance <= 1:
            return False

        dx = target.position.x - monster.position.x
        dy = target.position.y - monster.position.y

        # Вычисляем новую позицию, двигаясь на 1 шаг ближе
        new_x = monster.position.x + (1 if dx > 0 else -1 if dx < 0 else 0)
        new_y = monster.position.y + (1 if dy > 0 else -1 if dy < 0 else 0)

        # Проверяем границы карты

        if self.game_map.is_passable(Position(new_x, new_y)):
            monster.position = Position(new_x, new_y)
            return True
        return False