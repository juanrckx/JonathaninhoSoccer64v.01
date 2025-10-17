import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class GameScreen:
    def __init__(self, game_config):
        self.running = True
        pygame.display.set_caption("Jonathaninho Soccer 64 - Partida")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game_config = game_config
        self.background_image = self.load_image("background_image.png")

        self.score = {"local": 0, "visit": 0}
        self.current_turn = "local"
        self.game_state = "playing" #playing, goal, finished

    def load_image(self, file_path):
        image_path = os.path.join(IMAGES_DIR, file_path)
        return pygame.image.load(image_path)

    def draw(self):
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Negro semi-transparente (alpha = 128/255)
            screen.blit(overlay, (0, 0))
        else:
            screen.fill(BACKGROUND_COLOR)


        score_text = title_font.render(f"{self.score['local']} - {self.score['visit']}", True, YELLOW)
        screen.blit(score_text, (SCREEN_CENTER[0] - score_text.get_width() // 2, 50))

        turn_text = header_font.render(f"Turno: {self.current_turn.upper()}", True, WHITE)
        self.screen.blit(turn_text, (SCREEN_CENTER[0] - turn_text.get_width() // 2, 120))

        #Instrucciones
        help_text = small_font.render("Presione 1-6 para disparar | ESC para volver", True, WHITE)
        self.screen.blit(help_text, (SCREEN_CENTER[0] - help_text.get_width() // 2, SCREEN_HEIGHT - 50))

        pygame.display.flip()

    def handle_shot(self, paddle):
        self.score[self.current_turn] += 1


        self.current_turn = "visit" if self.current_turn == "local" else "local"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'back'

                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                    paddle = event.key - pygame.K_1  # 0-5
                    self.handle_shot(paddle)


        return "game"

    def run(self):
        while self.running:
            action = self.handle_events()
            if action != "game":
                return action

            self.draw()
            pygame.time.Clock().tick(60)