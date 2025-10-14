import pygame
import os

pygame.init()

DARK_GREEN = (15, 30, 15)
GREEN = 124,252,0
YELLOW = 220, 220, 0
WHITE = 255, 255, 255
LIGHT_BLUE = 0, 200, 255
BLUE = 0, 0, 255

BREATH_MIN_ALPHA = 100
BREATH_MAX_ALPHA = 255
BREATH_SPEED = 5.0

info = pygame.display.Info()
MONITOR_WIDTH = info.current_w
MONITOR_HEIGHT = info.current_h

MIN_WIDTH, MIN_HEIGHT = 1024, 768
MAX_WIDTH, MAX_HEIGHT = 1920, 1080

SCREEN_WIDTH = max(MIN_WIDTH, min(MAX_WIDTH, MONITOR_WIDTH - 100))
SCREEN_HEIGHT = max(MIN_HEIGHT, min(MAX_HEIGHT, MONITOR_HEIGHT - 100))
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jonathaninho Soccer 64 - Acerca de")

SCALE_X = SCREEN_WIDTH / 1600
SCALE_Y = SCREEN_HEIGHT / 900
SCALE_FACTOR = min(SCALE_X, SCALE_Y)

title_font = pygame.font.Font(None, int(72 * SCALE_FACTOR))
header_font = pygame.font.Font(None, int(48 * SCALE_FACTOR))
text_font = pygame.font.Font(None, int(32 * SCALE_FACTOR))
small_font = pygame.font.Font(None, int(24 * SCALE_FACTOR))



BACKGROUND_COLOR = DARK_GREEN
TITLE_COLOR = YELLOW
TEXT_COLOR = WHITE
HIGHLIGHT_COLOR = LIGHT_BLUE
BUTTON_COLOR = BLUE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")
#FONTS_DIR = os.path.join(BASE_DIR, "fonts")

#Funciones de ayuda para posiciones responsivas
def responsive_x(x):
    #Convierte coordenada X a coordenada real
    return int(x * SCALE_X)

def responsive_y(y):
    #Convierte coordenada Y a coordenada real
    return int(y * SCALE_Y)

def responsive_size(width, height):
    #Convierte tamano del diseno base a tamano real
    return int(width * SCALE_FACTOR), int(height * SCALE_FACTOR)

def responsive_rect(x, y, width, height):
    #Crea un rectangulo responsible
    return pygame.Rect(responsive_x(x), responsive_y(y), int(width * SCALE_FACTOR), int(height * SCALE_FACTOR))