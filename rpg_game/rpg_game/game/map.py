# game/map.py
from rpg_game.entities import Position


class Tile:
    def __init__(self, terrain_type: str = 'grass', objects: list = None):
        self.terrain_type = terrain_type
        self.objects = objects or []  # 'tree', 'chest', 'stone'


class GameMap:
    def __init__(self, size: int):
        self.size = size
        self.tiles = [[Tile() for _ in range(size)] for _ in range(size)]

    def set_tile(self, x: int, y: int, terrain: str, objects: list = None):
        self.tiles[y][x] = Tile(terrain, objects or [])

    def is_passable(self, position: Position) -> bool:
        if 0 <= position.x < self.size and 0 <= position.y < self.size:
            tile = self.tiles[position.y][position.x]
            return 'rock' not in tile.objects and 'tree' not in tile.objects
        else:
            return False