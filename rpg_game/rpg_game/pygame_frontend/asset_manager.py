# pygame_frontend/asset_manager.py
import pygame
from pathlib import Path
from typing import Optional

class AssetManager:
    def __init__(self):
        self.sprites = {}
        self.base_path = Path(__file__).parent.parent.parent / "assets" / "sprites"

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