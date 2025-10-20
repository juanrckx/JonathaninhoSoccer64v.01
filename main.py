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

class AudioManager:
    def __init__(self):
        self.current_music = None
        self.sounds = {}


    def load_sounds(self):
        self.sounds["whistle"] = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, WHISTLE_SOUND))
        self.sounds["cheer"] = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, CHEER_SOUND))
        self.sounds["boo"] = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, BOO_SOUND))

    def play_music(self, music_file, loops=-1):
        if self.current_music != music_file:
            pygame.mixer.music.load(os.path.join(SOUNDS_DIR, music_file))
            pygame.mixer.music.play(loops)
            self.current_music = music_file

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()


def main():
    # Inicializar la ventana principal
    pygame.display.set_caption("Jonathaninho Soccer 64")

    pygame.mixer.init()
    audio_manager = AudioManager()
    audio_manager.load_sounds()

    # Instanciar pantallas
    main_menu = MainMenu(audio_manager)
    about_screen = AboutScreen(audio_manager)
    instructions_screen = InstructionsScreen(audio_manager)
    config_screen = ConfigScreen(audio_manager)


    # Navegación entre pantallas
    current_screen = "main_menu"
    coin_toss_screen = None
    game_config = None

    #Reproducir musica de fondo inicial
    audio_manager.play_music(BACKGROUND_MUSIC)

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
                coin_toss_screen = CoinTossScreen(game_config, audio_manager)
                current_screen = "coin_toss"
            elif action == "back" or action == "quit":
                current_screen = "main_menu"

        elif current_screen == "coin_toss":
            # Cambiar música para el sorteo
            audio_manager.play_music(GAME_MUSIC)
            action, updated_config = coin_toss_screen.run()
            if action == "start_game":
                game_config = updated_config
                game_screen = GameScreen(game_config, audio_manager)
                # Restaurar música principal
                audio_manager.play_music(GAME_MUSIC)
                current_screen = "game"
            elif action == "back" or action == "quit":
                # Restaurar música principal
                audio_manager.play_music(BACKGROUND_MUSIC)
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