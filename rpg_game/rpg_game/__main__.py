# main.py
from pyexpat.errors import messages

from pygame_frontend.window import PygameWindow
from pygame_frontend.renderer import PygameRenderer
from pygame_frontend.input_handler import PygameInputHandler
from game.game import Game
from rpg_game.my_logging import Logger

import pygame


def main():
    Logger().initialize()
    Logger().info("Запуск игры")
    window = PygameWindow()
    renderer = PygameRenderer(window.screen)
    input_handler = PygameInputHandler()
    game = Game(renderer, input_handler)

    game.run()

    window.close()



if __name__ == "__main__":
    main()