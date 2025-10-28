import pygame
import os

pygame.init()

GREEN = 124,252,0
YELLOW = 220, 220, 0
WHITE = 255, 255, 255
LIGHT_BLUE = 0, 200, 255
BLUE = 0, 0, 255
RED = 255, 0, 0

#HARDWARE
WIFI_CONFIG = {'ssid': 'Casa4',
               'password': 'cartago04'}

HARDWARE_CONFIG = {
    'potentiometer': 26,
    'buttons': [15, 14, 13],
    'palettes': [1, 2, 3, 4, 5, 6],
    'leds': [8, 9, 10, 11, 12, 13],
    'status_led': 25
}

SERVER_CONFIG = {'port': 1717,
                 'timeout': 10}

# Rutas de archivos de audio
BACKGROUND_MUSIC = "background_music.mp3"
GAME_MUSIC = "game_music.mp3"
WHISTLE_SOUND = "whistle.mp3"
CHEER_SOUND = "cheer.mp3"
BOO_SOUND = "boo.mp3"

BREATH_MIN_ALPHA = 100
BREATH_MAX_ALPHA = 255
BREATH_SPEED = 5.0

title_font = pygame.font.Font(None, 48)
header_font = pygame.font.Font(None, 36)
text_font = pygame.font.Font(None, 28)
small_font = pygame.font.Font(None, 24)

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jonathaninho Soccer 64 - Acerca de")

BACKGROUND_COLOR = GREEN
TITLE_COLOR = YELLOW
TEXT_COLOR = WHITE
HIGHLIGHT_COLOR = LIGHT_BLUE
BUTTON_COLOR = BLUE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")
#FONTS_DIR = os.path.join(BASE_DIR, "fonts")