# game/map.py
from rpg_game.entities import Position, DrawableEntity
from rpg_game.game.events import Events

from abc import ABC, abstractmethod


class Tile:
    def __init__(self, terrain_type: str = 'grass'):
        self.layers = {
            'terrain': terrain_type,  # Тип земли (grass/stone/water)
            'objects': [],  # Статичные объекты (tree/stone)
            'entities': [],  # Сущности (игрок/монстры)
            'effects': []  # Временные эффекты (огонь/искры)
        }

    def set_layer (self, layer: str, objects: list = None):
        self.layers[layer] = objects or []

    def get_layer (self, layer:str):
        return self.layers[layer]

    def is_passable(self) -> bool:
        """Проверяет, можно ли перемещаться через клетку.

        Клетка непроходима, если содержит:
        - Статические объекты (камни, деревья)
        - Другие сущности (игроки, монстры)
        """
        has_blocking_objects = bool(self.layers['objects'])
        has_entities = bool(self.layers['entities'])
        return not (has_blocking_objects or has_entities)


class IGameMap(ABC):
    @abstractmethod
    def get_tile(self, x: int, y: int) -> Tile:
        pass

    @abstractmethod
    def get_entities(self) -> list[DrawableEntity]:
        pass

    @abstractmethod
    def get_size(self) -> (int, int):
        pass

    @abstractmethod
    def get_player(self) -> DrawableEntity:
        pass


class GameMap:
    def __init__(self,
                 map_width: int,
                 map_height: int):
        self.width = map_width
        self.height = map_height
        self.tiles = [[Tile() for _ in range(self.width)] for _ in range(self.height)]
        self.entities = []  # Новый слой для сущностей (динамические объекты)
        self._subscribe_to_events()
        self.player = None

    def _subscribe_to_events(self):
        Events.ENTITY_CREATED.subscribe(self._handle_entity_created)
        Events.ENTITY_MOVED.subscribe(self._handle_entity_moved)
        Events.ENTITY_DIED.subscribe(self._handle_entity_died)

    def _handle_entity_created(self, entity):
        x, y = entity.position.x, entity.position.y
        self.set_tile_layer(x, y, 'entities', [entity])

    def _handle_entity_moved(self, entity, old_pos, new_pos):
        self.set_tile_layer(old_pos.x, old_pos.y, 'entities',[])
        self.set_tile_layer(new_pos.x, new_pos.y, 'entities', [entity])

    def _handle_entity_died(self, entity):
        x, y = entity.position.x, entity.position.y
        self.set_tile_layer(x, y, 'entities',[])

    def init_tile(self, x: int, y: int, terrain: str, layer: str, objects: list = None):
        new_tile = Tile(terrain)
        new_tile.set_layer(layer, objects)
        self.tiles[y][x] = new_tile

    def set_tile_layer (self, x: int, y: int, layer: str, objects: list = None):
        self.tiles[y][x].set_layer(layer, objects)

    def is_passable(self, position: Position) -> bool:
        if 0 <= position.x < self.width and 0 <= position.y < self.height:
            tile = self.tiles[position.y][position.x]
            return tile.is_passable()
        else:
            return False

    def get_size(self) -> (int, int):
        return self.width, self.height

    def get_tile(self, x: int, y: int) -> Tile:
        return self.tiles[x][y]

    def get_entities(self) -> list[DrawableEntity]:
        return self.entities

    def set_player(self, player: DrawableEntity):
        self.player = player

    def get_player(self) -> DrawableEntity:
        return self.player

    def add_entity(self, entity: DrawableEntity):
        self.entities.append(entity)

    def remove_entity(self, entity: DrawableEntity):
        self.entities.remove(entity)