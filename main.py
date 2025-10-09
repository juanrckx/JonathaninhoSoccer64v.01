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


def main():
    # Inicializar la ventana principal
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jonathaninho Soccer 64")

    # Instanciar pantallas
    main_menu = MainMenu()
    about_screen = AboutScreen()
    instructions_screen = InstructionsScreen()
    config_screen = ConfigScreen()
    game_config = None

    # Navegación entre pantallas
    current_screen = "main_menu"

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

        elif current_screen == "config":
            action, config = config_screen.run()
            if action == "start_game":
                game_config = config
                print("Configuracion:", game_config)
                current_screen = "coin_toss"
            elif action == "back" or action == "quit":
                current_screen = "main_menu"

        elif current_screen == "instructions":
            action = instructions_screen.run()
            if action == "back" or action == "quit":
                current_screen = "about"

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()