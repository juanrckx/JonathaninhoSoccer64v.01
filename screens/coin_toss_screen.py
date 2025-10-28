import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class CoinTossScreen:
    def __init__(self, game_config, audio_manager=None, hardware_manager=None):
        self.running = True
        pygame.display.set_caption("Jonathaninho Soccer 64")
        self.audio_manager = audio_manager
        self.hardware_manager = hardware_manager

        self.background_image = self.load_image("background_image.png")
        self.game_config = game_config
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        #Estados de la animacion
        self.animation_state = "tossing" # "tossing", "result", "complete"
        self.coin_angle = 0
        self.coin_rotation_speed = 0
        self.coin_y = SCREEN_HEIGHT // 3
        self.coin_velocity = 0
        self.gravity = 0.5
        self.bounce_count = 0
        self.max_bounces = 3

        #Resultados
        self.result = None
        self.local_team = None
        self.visit_team = None

        #Tiempos
        self.animation_timer = 0
        self.result_timer = 0

    def load_image(self, file_name):
        image_path = os.path.join(IMAGES_DIR, file_name)
        if os.path.exists(image_path):
            background = pygame.image.load(image_path)
            return pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        return None

    def draw_coin(self):
        coin_radius = 60
        coin_x = SCREEN_WIDTH // 2

        #Dibujar moneda
        pygame.draw.circle(screen, YELLOW, (coin_x, self.coin_y), coin_radius)
        pygame.draw.circle(screen, YELLOW, (coin_x, self.coin_y), coin_radius, 3)

        #Cara
        if int(self.coin_angle / 100) % 2 == 0:
            pygame.draw.circle(screen, (180, 180, 0), (coin_x, self.coin_y), coin_radius - 10)
            face_text = header_font.render("C", True, (100, 100, 0))
        #Cruz
        else:
            pygame.draw.circle(screen, (160, 160, 0), (coin_x, self.coin_y), coin_radius - 10)
            face_text = header_font.render("S", True, (100, 100, 0))

        #Rotar texto
        rotated_text = pygame.transform.rotate(face_text, self.coin_angle)
        text_rect = rotated_text.get_rect(center=(coin_x, self.coin_y))
        screen.blit(rotated_text, text_rect)

    def draw_teams_info(self):
        local_team_data = self.game_config["team_local"]
        visit_team_data = self.game_config["team_visit"]

        #Titulo
        title_text = header_font.render("Sorteo de Moneda", True, (100, 100, 0))
        self.screen.blit(title_text, (SCREEN_CENTER[0] - title_text.get_width()//2, 30))

        # Equipos participantes
        teams_text = header_font.render("Equipos Participantes", True, LIGHT_BLUE)
        self.screen.blit(teams_text, (SCREEN_CENTER[0] - teams_text.get_width()//2, 100))

        # Nombres de equipos
        local_name = text_font.render(f"{local_team_data['name']}", True, WHITE)
        visit_name = text_font.render(f"{visit_team_data['name']}", True, WHITE)

        self.screen.blit(local_name, (SCREEN_CENTER[0] - 300, 150))
        self.screen.blit(visit_name, (SCREEN_CENTER[0] + 100, 150))

        # Escudos
        try:
            local_shield = pygame.image.load(os.path.join(IMAGES_DIR, local_team_data["shield"]))
            visit_shield = pygame.image.load(os.path.join(IMAGES_DIR, visit_team_data["shield"]))

            local_shield = pygame.transform.scale(local_shield, (80, 80))
            visit_shield = pygame.transform.scale(visit_shield, (80, 80))

            self.screen.blit(local_shield, (SCREEN_CENTER[0] - 400, 140))
            self.screen.blit(visit_shield, (SCREEN_CENTER[0] + 230, 140))
        except:
            pass

    def draw_result(self):
        if not self.result:
            return

        result_y = SCREEN_HEIGHT // 2 + 100

        # Título del resultado
        result_title = header_font.render("¡Resultado del Sorteo!", True, YELLOW)
        self.screen.blit(result_title, (SCREEN_CENTER[0] - result_title.get_width() // 2, result_y))

        # Equipo local
        local_text = text_font.render(f"Equipo Local: {self.local_team['name']}", True, LIGHT_BLUE)
        self.screen.blit(local_text, (SCREEN_CENTER[0] - local_text.get_width() // 2, result_y + 50))

        # Equipo visitante
        visit_text = text_font.render(f"Equipo Visitante: {self.visit_team['name']}", True, LIGHT_BLUE)
        self.screen.blit(visit_text, (SCREEN_CENTER[0] - visit_text.get_width() // 2, result_y + 90))

        # Instrucción para continuar
        continue_text = small_font.render("Presione ESPACIO para continuar al juego", True, (200, 200, 200))
        self.screen.blit(continue_text, (SCREEN_CENTER[0] - continue_text.get_width() // 2, SCREEN_HEIGHT - 50))

    def draw_instructions(self):
        """Dibuja instrucciones durante la animación"""
        if self.animation_state == "tossing":
            instr_text = small_font.render("Lanzando moneda...", True, (200, 200, 200))
            self.screen.blit(instr_text, (SCREEN_CENTER[0] - instr_text.get_width() // 2, SCREEN_HEIGHT - 50))

    def update_animation(self):
        """Actualiza la animación de la moneda"""
        if self.animation_state == "tossing":
            # Rotación
            self.coin_angle += self.coin_rotation_speed
            self.coin_rotation_speed = max(0, int(self.coin_rotation_speed - 0.5))

            # Física de salto
            self.coin_velocity += self.gravity
            self.coin_y += self.coin_velocity

            # Rebote en el "suelo"
            if self.coin_y > SCREEN_HEIGHT // 2 + 50:
                self.coin_y = SCREEN_HEIGHT // 2 + 50
                self.coin_velocity = -self.coin_velocity * 0.7  # Rebote con pérdida de energía
                self.bounce_count += 1

                # Sonido de rebote (podrías agregar un sonido aquí)
                if self.bounce_count <= self.max_bounces:
                    pass  # pygame.mixer.Sound("bounce.wav").play()

            # Terminar animación cuando se detenga
            if self.coin_rotation_speed <= 0 and self.bounce_count >= self.max_bounces:
                self.animation_state = "result"
                self.determine_winner()
                self.result_timer = pygame.time.get_ticks()

        elif self.animation_state == "result":
            # Esperar un momento antes de mostrar resultado
            if pygame.time.get_ticks() - self.result_timer > 1000:
                self.animation_state = "complete"

    def determine_winner(self):
        """Determina aleatoriamente qué equipo es local y cuál visitante"""
        # 50% de probabilidad para cada equipo
        if random.random() < 0.5:
            self.result = "local_wins"
            self.local_team = self.game_config["team_local"]
            self.visit_team = self.game_config["team_visit"]
        else:
            self.result = "visit_wins"
            self.local_team = self.game_config["team_visit"]
            self.visit_team = self.game_config["team_local"]

        # Actualizar la configuración del juego
        self.game_config["team_local"] = self.local_team
        self.game_config["team_visit"] = self.visit_team

    def draw(self):
        """Dibuja toda la pantalla de sorteo"""
        # Fondo
        self.screen.blit(self.background_image, (0, 0))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))


        # Información de equipos
        self.draw_teams_info()

        # Moneda animada
        self.draw_coin()

        # Resultado o instrucciones
        if self.animation_state in ["result", "complete"]:
            self.draw_result()
        else:
            self.draw_instructions()

        pygame.display.flip()

    def handle_events(self):
        """Maneja eventos de la pantalla de sorteo"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
                elif event.key == pygame.K_SPACE:
                    if self.animation_state == "complete":
                        return "start_game"
                elif event.key == pygame.K_RETURN:
                    # Iniciar animación si no ha comenzado
                    if self.animation_state == "tossing" and self.coin_rotation_speed == 0:
                        self.coin_rotation_speed = 25
                        self.coin_velocity = -15
                        self.coin_y = SCREEN_HEIGHT // 3

        if self.hardware_manager and self.hardware_manager.connected:
            # Crear copia temporal para evitar cambios durante la verificación
            button_states = self.hardware_manager.button_states.copy()

            # BTN1: SOLO iniciar juego - con protección contra detección múltiple
            if button_states.get("btn1") and self.animation_state == "complete":
                self.hardware_manager.button_states["btn1"] = False
                return "start_game"

        return "coin_toss"

    def run(self):
        """Ejecuta la pantalla de sorteo"""
        # Iniciar animación automáticamente después de un breve momento
        pygame.time.delay(500)

        while self.running:
            action = self.handle_events()
            if action != "coin_toss":
                return action, self.game_config

            self.update_animation()
            self.draw()
            pygame.time.Clock().tick(60)
        return None