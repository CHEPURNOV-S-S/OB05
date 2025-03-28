# main.py
from pyexpat.errors import messages

from pygame_frontend.window import PygameWindow
from pygame_frontend.renderer import PygameRenderer
from pygame_frontend.input_handler import PygameInputHandler
from game.game import Game
from rpg_game.my_logging import Logger
from rpg_game.game.events import Events

import pygame


def main():
    Logger().initialize()
    Events().initialize()
    Logger().info("Создание окна")
    window = PygameWindow()

    Logger().info("Создание рендера")
    renderer = PygameRenderer(window.screen)

    Logger().info("Создание обработчика ввода")
    input_handler = PygameInputHandler()

    Logger().info("Инициализация игры")
    game = Game(renderer, input_handler)

    Logger().info("Старт игры")
    game.run()

    Logger().info("Закрытие окна")
    window.close()



if __name__ == "__main__":
    main()