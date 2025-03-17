# game/constants.py

MAP_WIDTH = 15    # Ширина карты в тайлах
MAP_HEIGHT = 10   # Высота карты в тайлах
TILE_SIZE = 64    # Размер тайла в пикселях

STATUS_PANEL_HEIGHT = 225  # Размер панели статуса.

# Размер экрана:
SCREEN_WIDTH  = (MAP_WIDTH  + 1) * TILE_SIZE
SCREEN_HEIGHT = (MAP_HEIGHT + 1) * TILE_SIZE + STATUS_PANEL_HEIGHT
FPS = 60
MAX_AP = 5
TELEPORT_COST = 3