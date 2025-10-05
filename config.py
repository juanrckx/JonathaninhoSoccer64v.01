import pygame
import os

pygame.init()

GREEN = 15, 30, 15
YELLOW = 220, 220, 0
WHITE = 255, 255, 255
LIGHT_BLUE = 0, 200, 255
BLUE = 0, 0, 255

BREATH_MIN_ALPHA = 100
BREATH_MAX_ALPHA = 255
BREATH_SPEED = 5.0

title_font = pygame.font.Font(None, 48)
header_font = pygame.font.Font(None, 36)
text_font = pygame.font.Font(None, 28)
small_font = pygame.font.Font(None, 24)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jonathaninho Soccer 64 - Acerca de")

BACKGROUND_COLOR = GREEN
TITLE_COLOR = YELLOW
TEXT_COLOR = WHITE
HIGHLIGHT_COLOR = LIGHT_BLUE
BUTTON_COLOR = BLUE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
#FONTS_DIR = os.path.join(BASE_DIR, "fonts")