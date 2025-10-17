import random

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

        self.shots_taken = {"local": 0, "visit": 0}
        self.max_shots = 5
        self.current_phase = "waiting_shot"

        self.goalkeeper_position = None
        self.last_shot_position = None
        self.last_shot_result = None

        self.result_timer = 0
        self.result_duration = 2000

        self.player_stats = {"local": {"goals": 0, "shots": 0},
                             "visit": {"goals": 0, "shots": 0}}

    def load_image(self, file_path):
        image_path = os.path.join(IMAGES_DIR, file_path)
        return pygame.image.load(image_path)

    def generate_goalkeeper_position(self):
        goalkeeper_key = "goalie_local" if self.current_turn == "local" else "goalie_visit"

        goalkeeper_index = self.game_config[goalkeeper_key]

        positions = [#AN1: 2 paletas contiguas (3 grupos posibles)
                    [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]],
                    #AN2: 3 paletas contiguas (2 grupos posibles)
                    [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5]],
                    #AN3: 3 paletas alternas (2 grupos posibles)
                    [[0, 2, 4], [1, 3, 5]]]


        position_group = positions[goalkeeper_index % len(positions)]
        return random.choice(position_group)

    def check_goal(self, shot_position):
        for covered_position in self.goalkeeper_position:
            if shot_position == covered_position:
                return False
            return True

    def handle_shot(self, shot_position):
        #Generar portero para el turno
        self.goalkeeper_position = self.generate_goalkeeper_position()

        #Verificar si es gol
        is_goal = self.check_goal(shot_position)
        self.last_shot_position = shot_position
        self.last_shot_result = is_goal

        #Actualizar marcador
        if is_goal:
            self.score[self.current_turn] += 1
            self.player_stats[self.current_turn]["goals"] += 1

        self.player_stats[self.current_turn]["shots"] += 1
        self.shots_taken[self.current_turn] += 1

        #Cambiar a fase de mostrar resultado
        self.current_phase = "showing_result"
        self.result_timer = pygame.time.get_ticks()

        #Determinar siguiente estado
        if self.shots_taken[self.current_turn] >= self.max_shots:
            if all(shots >= self.max_shots for shots in self.shots_taken.values()):
                self.game_state = "finished"

            else:
                self.current_turn = "visit" if self.current_turn == "local" else "local"

        return is_goal

    def draw_goalkeeper_indicator(self):
        if self.goalkeeper_position and self.current_phase == "showing_result":
            goalie_y = SCREEN_HEIGHT // 2 + 50
            for i in range(6):
                color = RED if i in self.goalkeeper_position else GREEN
                pygame.draw.rect(self.screen, color, (200 + i * 80, goalie_y, 60, 20))

            goalie_text = small_font.render("Posicion del Portero", True, WHITE)
            self.screen.blit(goalie_text, (200, goalie_y - 30))

    def draw_shot_result(self):
        if self.current_phase == "showing_result" and self.last_shot_result is not None:
            result_y = SCREEN_HEIGHT // 2 - 100

            if self.last_shot_result:
                result_text = title_font.render("GOL!", True, YELLOW)
                message = "Anotacion valida!"

            else:
                result_text = title_font.render("ATAJADO!", True, RED)
                message = "Portero cubrio la posicion"

            self.screen.blit(result_text, (SCREEN_CENTER[0] - result_text.get_width() // 2, result_y))

            message_text = header_font.render(message, True, WHITE)
            self.screen.blit(message_text, (SCREEN_CENTER[0] - message_text.get_width() // 2, result_y + 60))

            # Mostrar posición del tiro
            shot_text = text_font.render(f"Tiro en paleta: {self.last_shot_position + 1}", True, LIGHT_BLUE)
            self.screen.blit(shot_text, (SCREEN_CENTER[0] - shot_text.get_width() // 2, result_y + 110))

    def draw_scoreboard(self):
        score_text = title_font.render(f"{self.score['local']} - {self.score['visit']}", True, YELLOW)
        self.screen.blit(score_text, (SCREEN_CENTER[0] - score_text.get_width() // 2, 50))

        # Información de turno
        turn_text = header_font.render(f"Turno: {self.current_turn.upper()}", True, WHITE)
        self.screen.blit(turn_text, (SCREEN_CENTER[0] - turn_text.get_width() // 2, 120))

        # Tiros realizados
        shots_text = text_font.render(
            f"Tiros: Local {self.shots_taken['local']}/{self.max_shots} | Visitante {self.shots_taken['visit']}/{self.max_shots}",
            True, LIGHT_BLUE
        )
        self.screen.blit(shots_text, (SCREEN_CENTER[0] - shots_text.get_width() // 2, 160))

    def draw_goal_display(self):
        goal_y = SCREEN_HEIGHT // 2 - 50
        goal_width = 500

        pygame.draw.rect(self.screen, WHITE, (SCREEN_CENTER[0] - goal_width // 2, goal_y, goal_width, 100), 2)

        # Dibujar paletas (1-6)
        for i in range(6):
            palette_x = SCREEN_CENTER[0] - goal_width // 2 + (i * (goal_width // 6))

            # Resaltar la última paleta disparada
            if self.last_shot_position == i and self.current_phase == "showing_result":
                color = YELLOW if self.last_shot_result else RED
                pygame.draw.rect(self.screen, color, (palette_x, goal_y, goal_width // 6, 100))

            # Número de paleta
            num_text = text_font.render(str(i + 1), True, WHITE)
            self.screen.blit(num_text, (palette_x + (goal_width // 12) - num_text.get_width() // 2, goal_y + 40))

    def draw_game_finished(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        if self.score["local"] > self.score["visit"]:
            result_msg = "EQUIPO LOCAL GANA!"
        elif self.score["local"] < self.score["visit"]:
            result_msg = "EQUIPO VISITANTE GANA!"
        else:
            result_msg = "EMPATE!"

        result_text = title_font.render(result_msg, True, YELLOW)
        self.screen.blit(result_text, (SCREEN_CENTER[0] - result_text.get_width() // 2, SCREEN_CENTER[1] - 100))

        # Marcador final
        score_text = header_font.render(f"Resultado Final: {self.score['local']} - {self.score['visit']}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_CENTER[0] - score_text.get_width() // 2, SCREEN_CENTER[1] - 30))

        # Estadísticas
        local_accuracy = (self.player_stats["local"]["goals"] / max(self.player_stats["local"]["shots"], 1)) * 100
        visit_accuracy = (self.player_stats["visit"]["goals"] / max(self.player_stats["visit"]["shots"], 1)) * 100

        stats_text = text_font.render(
            f"Precisión: Local {local_accuracy:.1f}% | Visitante {visit_accuracy:.1f}%",
            True, LIGHT_BLUE
        )
        self.screen.blit(stats_text, (SCREEN_CENTER[0] - stats_text.get_width() // 2, SCREEN_CENTER[1] + 30))

        # Instrucciones para continuar
        continue_text = small_font.render("Presione ESPACIO para volver al menú principal", True, WHITE)
        self.screen.blit(continue_text, (SCREEN_CENTER[0] - continue_text.get_width() // 2, SCREEN_HEIGHT - 100))

    def draw(self):
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Negro semi-transparente (alpha = 128/255)
            screen.blit(overlay, (0, 0))
        else:
            screen.fill(BACKGROUND_COLOR)

        if self.game_state == "finished":
            self.draw_game_finished()
        else:
            self.draw_scoreboard()
            self.draw_goal_display()

            if self.current_phase == "showing_result":
                self.draw_shot_result()
                self.draw_goalkeeper_indicator()

            if self.current_phase == "waiting_shot":
                help_text = small_font.render("Presione 1-6 para disparar | ESC para volver", True, WHITE)
                self.screen.blit(help_text, (SCREEN_CENTER[0] - help_text.get_width() // 2, SCREEN_HEIGHT - 50))

        pygame.display.flip()

    def update(self):
      if self.current_phase == "showing_result":
          if pygame.time.get_ticks() - self.result_timer > self.result_duration:
              self.current_phase = "waiting_shot"
              self.last_shot_result = None


    def handle_events(self):
        """Maneja eventos de la pantalla de juego"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'back'

                elif event.key == pygame.K_SPACE and self.game_state == "finished":
                    return 'back'

                elif self.current_phase == "waiting_shot" and self.game_state == "playing":
                    # Detectar tiros con teclas 1-6
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                        shot_position = event.key - pygame.K_1  # Convertir a 0-5
                        self.handle_shot(shot_position)

        return "game"


    def run(self):
        """Ejecuta la pantalla de juego - CORREGIDO EL BUG"""
        while self.running:
            action = self.handle_events()
            if action != "game":  # ✅ CORREGIDO: Retorna cuando NO es "game"
                return action

            self.update()
            self.draw()
            pygame.time.Clock().tick(60)