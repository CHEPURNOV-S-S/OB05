# main.py
from pygame_frontend.window import PygameWindow
from pygame_frontend.renderer import PygameRenderer
from pygame_frontend.input_handler import PygameInputHandler
from game.game import Game
import pygame


def main():
    window = PygameWindow()
    renderer = PygameRenderer(window.screen)
    input_handler = PygameInputHandler()
    game = Game(renderer, input_handler)

    game.run()

    window.close()



if __name__ == "__main__":
    main()