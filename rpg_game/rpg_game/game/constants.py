# game/constants.py

MAP_WIDTH = 15    # Ширина карты в тайлах
MAP_HEIGHT = 10   # Высота карты в тайлах
TILE_SIZE = 64    # Размер тайла в пикселях

# Экран теперь рассчитывается правильно:
SCREEN_WIDTH = (MAP_WIDTH) * TILE_SIZE
SCREEN_HEIGHT = (MAP_HEIGHT) * TILE_SIZE
FPS = 60
MAX_AP = 5
TELEPORT_COST = 3