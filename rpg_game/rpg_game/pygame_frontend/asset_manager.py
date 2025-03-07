# pygame_frontend/asset_manager.py
import pygame
from pathlib import Path
from typing import Optional

class AssetManager:
    def __init__(self):
        self.sprites = {}
        self.base_path = Path(__file__).parent.parent.parent / "assets" / "sprites"
        self.terrain_mapping = {
            'grass': 'tiles/grass.png',
            'stone': 'tiles/stone.png',
            'water': 'tiles/water.png'  # Пример расширения
        }
        self.object_mapping = {
            'tree': 'objects/tree.png',
            'chest': 'objects/chest.png',
            'rock': 'objects/rock.png'  # Пример расширения
        }


    def get_sprite(self, name: str, scale: Optional[tuple[int, int]] = None):
        if name not in self.sprites:
            try:
                # Ленивая загрузка при первом запросе
                path = self.base_path / name
                sprite = pygame.image.load(path.as_posix()).convert_alpha()
                if scale:
                    sprite = pygame.transform.scale(sprite, scale)

            except FileNotFoundError:
                sprite = self.get_sprite("default.png")  # placeholder

            self.sprites[name] = sprite
        return self.sprites[name]

    def get_terrain_sprite(self, terrain_type: str):
        path = self.terrain_mapping.get(terrain_type, 'tiles/grass.png')
        return self.get_sprite(path)

    def get_object_sprite(self, object_type: str):
        path = self.object_mapping.get(object_type)
        return self.get_sprite(path) if path else None
