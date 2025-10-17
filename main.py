# main.py
import pygame
import sys
import os

# Agregar la carpeta screens al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'screens'))

from config import *
from screens.main_menu import MainMenu
from screens.about_screen import AboutScreen
from screens.config_screen import ConfigScreen
from screens.instructions_screen import InstructionsScreen
from screens.coin_toss_screen import CoinTossScreen
from screens.game_screen import GameScreen


def main():
    # Inicializar la ventana principal
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jonathaninho Soccer 64")

    # Instanciar pantallas
    main_menu = MainMenu()
    about_screen = AboutScreen()
    instructions_screen = InstructionsScreen()


    # Navegación entre pantallas
    current_screen = "main_menu"
    config_screen = ConfigScreen()
    coin_toss_screen = None
    game_config = None

    running = True
    while running:
        if current_screen == "main_menu":
            action = main_menu.run()
            if action == "about":
                current_screen = "about"
            elif action == "new_game":
                current_screen = "config"
            elif action == "config":
                current_screen = "config"
            elif action == "quit":
                running = False

        elif current_screen == "about":
            action = about_screen.run()
            if action == "instructions":
                current_screen = "instructions"
            elif action == "back" or action == "quit":
                current_screen = "main_menu"

        elif current_screen == "config":
            action, config = config_screen.run()
            if action == "start_game":
                game_config = config
                print("Configuracion:", game_config)
                coin_toss_screen = CoinTossScreen(game_config)
                current_screen = "coin_toss"
            elif action == "back" or action == "quit":
                current_screen = "main_menu"

        elif current_screen == "coin_toss":
            action, updated_config = coin_toss_screen.run()
            if action == "start_game":
                game_config = updated_config
                game_screen = GameScreen(game_config)
                current_screen = "game"
            elif action == "back" or action == "quit":
                current_screen = "main_menu"

        elif current_screen == "game":
            action = game_screen.run()
            if action == "back" or action == "quit":
                current_screen = "main_menu"

        elif current_screen == "instructions":
            action = instructions_screen.run()
            if action == "back" or action == "quit":
                current_screen = "about"

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()