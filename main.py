import pygame
import pygame
import sys
import os

# Agregar la carpeta screens al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'screens'))

from config import *
#from screens.main_menu import MainMenu
from screens.about_screen import AboutScreen
from screens.instructions_screen import InstructionsScreen

# Función principal para probar la pantalla
def main():
    current_screen = "about"
    about_screen = AboutScreen()
    instructions_screen = InstructionsScreen()

    while True:
        if current_screen == "about":
            result = about_screen.run()
            if result == "instructions":
                current_screen = "instructions"
            elif result == "back" or result == "quit":
                break

        elif current_screen == "instructions":
            result = instructions_screen.run()
            if result == "back":
                current_screen = "about"
            elif result == "quit":
                break
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()