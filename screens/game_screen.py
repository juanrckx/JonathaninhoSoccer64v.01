import random
import sys
import os

import pygame.time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class GameScreen:
    def __init__(self, game_config, audio_manager=None, hardware_manager=None):
        self.running = True
        pygame.display.set_caption("Jonathaninho Soccer 64 - Partida")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game_config = game_config
        self.background_image = self.load_image("background_image.png")
        self.audio_manager = audio_manager
        self.hardware_manager = hardware_manager
        self.hardware_shot_selection = 0
        self.setup_hardware_callbacks()

        #Estados del juego
        self.score = {"local": 0, "visit": 0}
        self.current_turn = "local"
        self.game_state = "cooldown" #playing, cooldown, finished, waiting_shot

        #Temporizadores
        self.cooldown_timer = pygame.time.get_ticks()
        self.cooldown_duration = 3000 # 3 segundos de preparacion

        self.shot_timer = 0
        self.shot_timeout = 5000 # 3 segundos para cobrar despues del pito
        self.shot_timer_active = False

        self.player_change_timer = 0
        self.auto_change_duration = 5000  # 5 segundos para cambio automatico

        self.shots_taken = {"local": 0, "visit": 0}
        self.max_shots = 5
        self.current_phase = "waiting_whistle"

        self.goalkeeper_position = None
        self.last_shot_position = None
        self.last_shot_result = None

        self.result_timer = 0
        self.result_duration = 2000

        self.finished_timer = 0
        self.finished_duration = 3000  # 3 segundos antes de ir a estadísticas

        self.player_stats = {"local": {"goals": 0, "shots": 0, "timeouts": 0},
                             "visit": {"goals": 0, "shots": 0, "timeouts": 0}}



        self.current_shooter_local = game_config.get("shooter_local", 0)
        self.current_shooter_visit = game_config.get("shooter_visit", 0)
        self.current_goalie_local = game_config.get("goalie_local", 0)
        self.current_goalie_visit = game_config.get("goalie_visit", 0)

        self.start_cooldown()

    def setup_hardware_callbacks(self):
        """Configura callbacks para el hardware durante el juego"""
        if self.hardware_manager and self.hardware_manager.connected:
            self.hardware_manager.register_callback("potentiometer", self.on_potentiometer_change)
            self.hardware_manager.register_callback("button", self.on_button_press)
            self.hardware_manager.register_callback("palette", self.on_palette_trigger)

    def on_potentiometer_change(self, value):
        """Selecciona paleta con potenciómetro durante el turno de tiro"""
        if self.current_phase == "waiting_shot":
            self.hardware_shot_selection = (value * 6) // 1024  # Mapear a 0-5

    def on_button_press(self, data):
        """Maneja botones durante el juego"""
        if data["button"] == "btn1" and data["state"]:
            if self.current_phase == "changing_players_manual":
                self.perform_player_change()

        elif data["button"] == "btn2" and data["state"]:
            # BTN2: Cambio manual de jugador
            if self.current_phase == "waiting_shot" and self.game_state == "playing":
                self.handle_shot(self.hardware_shot_selection)


    def on_palette_trigger(self, data):
        """MEJORA: Manejo robusto de detección de paletas"""
        palette_num = data["palette"]
        state = data["state"]

        # Solo procesar activaciones (state=True) durante el turno de tiro
        if state and self.current_phase == "waiting_shot" and self.game_state == "playing":
            self.handle_shot(palette_num)

    def start_cooldown(self):
        self.game_state = "cooldown"
        self.cooldown_timer = pygame.time.get_ticks()
        if self.audio_manager:
            self.audio_manager.play_sound("whistle")
        else:
            print("No se ha cargado el audio manager, no se ha ejecutado el sonido.")

    def start_shot_period(self):
        self.game_state = "playing"
        self.current_phase = "waiting_shot"
        self.shot_timer = pygame.time.get_ticks()
        self.shot_timer_active = True

        if self.audio_manager:
            self.audio_manager.play_sound("whistle")

        if self.hardware_manager:
            self.hardware_manager.send_command("CELEBRATE_STOP")

    def check_shot_timeout(self):
        if (self.shot_timer_active and
                self.current_phase == "waiting_shot" and
            pygame.time.get_ticks() - self.shot_timer > self.shot_timeout):

            self.handle_timeout_shot()
            return True
        return False

    def handle_timeout_shot(self):
        self.shot_timer_active = False
        self.last_shot_position = None
        self.last_shot_result = False

        self.player_stats[self.current_turn]["shots"] += 1
        self.player_stats[self.current_turn]["timeouts"] += 1
        self.shots_taken[self.current_turn] += 1

        #Mostrar resultado
        self.current_phase = "showing_result"
        self.result_timer = pygame.time.get_ticks()

        if self.audio_manager:
            self.audio_manager.play_sound("boo")

        self.handle_after_shot()

    def handle_shot(self, shot_position):
        # Generar portero para el turno
        self.goalkeeper_position = self.generate_goalkeeper_position()

        self.shot_timer_active = False

        # Verificar si es gol
        is_goal = self.check_goal(shot_position)
        self.last_shot_position = shot_position
        self.last_shot_result = is_goal

        # Actualizar marcador
        if self.audio_manager:
            if is_goal:
                self.score[self.current_turn] += 1
                self.player_stats[self.current_turn]["goals"] += 1
                self.audio_manager.play_sound("cheer")
                if self.hardware_manager:
                    self.hardware_manager.send_command("CELEBRATE_MAX")
            else:
                self.audio_manager.play_sound("boo")
                closeness = self.calculate_closeness_to_goal(shot_position)

                if self.hardware_manager:
                    if closeness > 0.8:
                        # Muy cerca del gol - 5 LEDs progresivos
                        self.hardware_manager.send_command("CELEBRATE:5")
                    elif closeness > 0.6:
                        # Cerca del gol - 4 LEDs progresivos
                        self.hardware_manager.send_command("CELEBRATE:4")
                    elif closeness > 0.4:
                        # Tiro medio - 3 LEDs progresivos
                        self.hardware_manager.send_command("CELEBRATE:3")
                    elif closeness > 0.2:
                        # Tiro lejano - 2 LEDs progresivos
                        self.hardware_manager.send_command("CELEBRATE:2")
                    else:
                        # Muy lejos - 1 LED progresivo
                        self.hardware_manager.send_command("CELEBRATE:1")

        self.player_stats[self.current_turn]["shots"] += 1
        self.shots_taken[self.current_turn] += 1

        # Cambiar a fase de mostrar resultado
        self.current_phase = "showing_result"
        self.result_timer = pygame.time.get_ticks()

        self.handle_after_shot()

    def calculate_closeness_to_goal(self, shot_position):
        """Calcular qué tan cerca estuvo el tiro de ser gol (0.0 a 1.0)"""
        if not self.goalkeeper_position:
            return 0.0

        # Si el portero cubre múltiples posiciones, calcular proximidad
        min_distance = 6  # Máxima distancia posible

        for covered_pos in self.goalkeeper_position:
            distance = abs(shot_position - covered_pos)
            if distance < min_distance:
                min_distance = distance

        # Convertir a valor entre 0.0 y 1.0 (1.0 = muy cerca, 0.0 = muy lejos)
        closeness = 1.0 - (min_distance / 3.0)  # Normalizar
        return max(0.0, min(1.0, closeness))

    def handle_after_shot(self):
        if self.game_state == "finished":
            return

        # Determinar siguiente estado
        if self.shots_taken[self.current_turn] >= self.max_shots:
            self.current_turn = "visit" if self.current_turn == "local" else "local"
            if all(shots >= self.max_shots for shots in self.shots_taken.values()):
                self.game_state = "finished"
                return

            if self.game_config.get("change_mode") == "auto":
                self.start_auto_change()
            else:
                self.current_phase = "changing_players_manual"

    def start_auto_change(self):
        self.current_phase = "changing_players_auto"
        self.auto_change_timer = pygame.time.get_ticks()

    def perform_player_change(self):
        if self.current_turn == "local":
            self.current_shooter_local = (self.current_shooter_local + 1) % 3
            self.current_goalie_local = (self.current_goalie_local + 1) % 3
        else:
            self.current_shooter_visit = (self.current_shooter_visit + 1) % 3
            self.current_goalie_visit = (self.current_goalie_visit + 1) % 3

        #Actualizar configuracion
        self.game_config["shooter_local"] = self.current_shooter_local
        self.game_config["goalie_local"] = self.current_goalie_local
        self.game_config["shooter_visit"] = self.current_shooter_visit
        self.game_config["goalie_visit"] = self.current_goalie_visit

        self.start_cooldown()

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.game_state == "cooldown":
            if current_time - self.cooldown_timer > self.cooldown_duration:
                self.start_shot_period()

        elif self.current_phase == "waiting_shot":
            self.check_shot_timeout()

        elif self.current_phase == "showing_result":
            if current_time - self.result_timer > self.result_duration:
                if self.game_config.get("change_mode") == "auto":
                    self.start_auto_change()
                else:
                    self.current_phase = "changing_players_manual"

        elif self.current_phase == "changing_players_auto":
            if current_time - self.auto_change_timer > self.auto_change_duration:
                self.perform_player_change()

        elif self.game_state == "finished":
            if current_time - self.finished_timer > self.finished_duration:
                return 'stats'

        return 'game'

    def draw_cooldown_message(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        cooldown_text = title_font.render("PREPÁRENSE!", True, YELLOW)
        self.screen.blit(cooldown_text, (SCREEN_CENTER[0] - cooldown_text.get_width() // 2, SCREEN_CENTER[1] - 140))

        time_left = max(0, self.cooldown_duration - (pygame.time.get_ticks() - self.cooldown_timer))
        seconds_left = (time_left // 1000) + 1

        countdown_text = header_font.render(str(seconds_left), True, WHITE)
        self.screen.blit(countdown_text, (SCREEN_CENTER[0] - countdown_text.get_width() // 2, SCREEN_CENTER[1] - 70))

        info_text = text_font.render("El juego comenzará en...", True, WHITE)
        self.screen.blit(info_text, (SCREEN_CENTER[0] - info_text.get_width() // 2, SCREEN_CENTER[1] - 100))

    def draw_shot_timer(self):
        if self.shot_timer_active and self.current_phase == "waiting_shot":
            time_left = max(0, self.shot_timeout - (pygame.time.get_ticks() - self.shot_timer))
            seconds_left = (time_left // 1000) + 1

            timer_y = SCREEN_HEIGHT - 100
            timer_text = header_font.render(f"TIEMPO: {seconds_left}", True, RED if seconds_left < 1 else YELLOW)

            self.screen.blit(timer_text, (SCREEN_CENTER[0] - timer_text.get_width() // 2, timer_y))

    def draw_player_change_indicator(self):
        if self.current_phase == "changing_players_auto":
            time_left = max(0, self.auto_change_duration - (pygame.time.get_ticks() - self.auto_change_timer))
            seconds_left = (time_left // 1000) + 1

            change_y = SCREEN_HEIGHT // 2 + 150
            change_text = header_font.render(f"CAMBIO AUTOMATICO EN: {seconds_left}", True, YELLOW)
            self.screen.blit(change_text, (SCREEN_CENTER[0] - change_text.get_width() // 2, change_y))

        elif self.current_phase == "changing_players_manual":
            change_y = SCREEN_HEIGHT // 2 + 150
            change_text = header_font.render(f"PRESIONE EL BOTON PARA CAMBIAR DE JUGADOR", True, YELLOW)

            self.screen.blit(change_text, (SCREEN_CENTER[0] - change_text.get_width() // 2, change_y))

            # Mostrar información del próximo jugador
            team_data = self.game_config["team_local"] if self.current_turn == "local" else self.game_config[
                "team_visit"]
            next_shooter_idx = (self.game_config[f"shooter_{self.current_turn}"] + 1) % 3
            next_goalie_idx = (self.game_config[f"goalie_{self.current_turn}"] + 1) % 3

            next_shooter = team_data["shooters"][next_shooter_idx]
            next_goalie = team_data["goalies"][next_goalie_idx]

            shooter_text = text_font.render(f"Próximo Artillero: {next_shooter['name']}", True, LIGHT_BLUE)
            goalie_text = text_font.render(f"Próximo Portero: {next_goalie['name']}", True, LIGHT_BLUE)

            self.screen.blit(shooter_text, (SCREEN_CENTER[0] - shooter_text.get_width() // 2, change_y + 40))
            self.screen.blit(goalie_text, (SCREEN_CENTER[0] - goalie_text.get_width() // 2, change_y + 70))

    def draw_current_players(self):
        #Local y visitante

        local_team = self.game_config["team_local"]
        local_shooter = local_team["shooters"][self.current_shooter_local]
        local_goalie = local_team["goalies"][self.current_goalie_local]

        #Visitante
        visit_team = self.game_config["team_visit"]
        visit_shooter =visit_team["shooters"][self.current_shooter_visit]
        visit_goalie = visit_team["goalies"][self.current_goalie_visit]

        y_pos = 200
        local_shooter_text = text_font.render(f"Artillero local: {local_shooter['name']}", True, YELLOW)
        local_goalie_text = text_font.render(f"Portero local: {local_goalie['name']}", True, YELLOW)

        visit_shooter_text = text_font.render(f"Artillero visitante: {visit_shooter['name']}", True, YELLOW)
        visit_goalie_text = text_font.render(f"Portero visitante: {visit_goalie['name']}", True, YELLOW)

        self.screen.blit(local_shooter_text, (50, y_pos))
        self.screen.blit(local_goalie_text, (50, y_pos + 20))

        self.screen.blit(visit_shooter_text, (650, y_pos))
        self.screen.blit(visit_goalie_text, (650, y_pos + 20))

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
        elif self.game_state == "cooldown":
            self.draw_cooldown_message()
            self.draw_scoreboard()
        else:
            self.draw_scoreboard()
            self.draw_current_players()
            self.draw_goal_display()

            if self.current_phase == "showing_result":
                self.draw_shot_result()
                self.draw_goalkeeper_indicator()

            self.draw_shot_timer()
            self.draw_player_change_indicator()

            if self.current_phase == "waiting_shot":
                help_text = small_font.render("Presione 1-6 para disparar | ESC para volver", True, WHITE)
                self.screen.blit(help_text, (SCREEN_CENTER[0] - help_text.get_width() // 2, SCREEN_HEIGHT - 50))

        pygame.display.flip()


    def handle_events(self):
        """Maneja eventos de la pantalla de juego"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'back'

                elif event.key == pygame.K_SPACE and self.game_state == "finished":
                    return 'stats'

                elif event.key == pygame.K_ESCAPE and self.game_state == "finished":
                    return 'back'

                elif self.current_phase == "waiting_shot" and self.game_state == "playing":
                    # Detectar tiros con teclas 1-6
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                        shot_position = event.key - pygame.K_1  # Convertir a 0-5
                        self.handle_shot(shot_position)

                elif self.current_phase == "changing_players_manual" and event.key == pygame.K_c:
                    self.perform_player_change()

        if self.hardware_manager and self.hardware_manager.button_states.get("btn3"):
            return "back"

        return "game"



    def load_image(self, file_path):
        image_path = os.path.join(IMAGES_DIR, file_path)
        return pygame.image.load(image_path)

    def generate_goalkeeper_position(self):
        """Genera la posición del portero según los índices AN"""
        goalkeeper_key = "goalie_local" if self.current_turn == "local" else "goalie_visit"
        goalkeeper_index = self.game_config[goalkeeper_key]

        # Los 3 índices AN del PDF (página 6) - CORREGIDOS
        positions = [
            # AN1: 2 paletas contiguas (5 grupos posibles)
            [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]],
            # AN2: 3 paletas contiguas (4 grupos posibles)
            [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5]],
            # AN3: 3 paletas alternas (2 grupos posibles)
            [[0, 2, 4], [1, 3, 5]]
        ]

        # Seleccionar grupo basado en el índice del portero
        position_group = positions[goalkeeper_index % len(positions)]
        return random.choice(position_group)

    def check_goal(self, shot_position):
        """Determina si es gol válido"""

        # Verificar si el tiro cayó en alguna de las paletas cubiertas por el portero
        for covered_palette in self.goalkeeper_position:
            if shot_position == covered_palette:
                return False  # Portero atajó

        return True  # GOL VÁLIDO

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

            if i == self.hardware_shot_selection and self.current_phase == "waiting_shot":
                pygame.draw.rect(self.screen, YELLOW, (palette_x, goal_y, goal_width // 6, 100), 3)            # Resaltar la última paleta disparada

            if self.last_shot_position == i and self.current_phase == "showing_result":
                color = YELLOW if self.last_shot_result else RED
                pygame.draw.rect(self.screen, color, (palette_x, goal_y, goal_width // 6, 100))

            # Número de paleta
            num_text = text_font.render(str(i + 1), True, WHITE)
            self.screen.blit(num_text, (palette_x + (goal_width // 12) - num_text.get_width() // 2, goal_y + 40))


    def draw_goalkeeper_indicator(self):
        if self.goalkeeper_position and self.current_phase == "showing_result":
            goalie_y = SCREEN_HEIGHT // 2 + 50
            for i in range(6):
                color = RED if i in self.goalkeeper_position else GREEN
                pygame.draw.rect(self.screen, color, (300 + i * 80, goalie_y, 70, 20))

            goalie_text = small_font.render("Posicion del Portero", True, WHITE)
            self.screen.blit(goalie_text, (460, goalie_y + 30))

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
            self.screen.blit(message_text, (SCREEN_CENTER[0] - message_text.get_width() // 2, result_y - 30))

            # Mostrar posición del tiro
            if self.last_shot_result is not None:
                shot_text = text_font.render(f"Tiro en paleta: {self.last_shot_position}", True, LIGHT_BLUE)
                self.screen.blit(shot_text, (SCREEN_CENTER[0] - shot_text.get_width() // 2, result_y - 55))

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


    def run(self):
        """Ejecuta la pantalla de juego"""
        while self.running:
            action = self.handle_events()
            if action != "game":
                return action

            update_result = self.update()
            if update_result != "game":
                return update_result

            self.draw()
            pygame.time.Clock().tick(60)
        return None