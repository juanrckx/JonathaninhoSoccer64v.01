import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *


class ConfigScreen:
    def __init__(self, audio_manager=None):
        self.running = True
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Jonathaninho Soccer 64 - Configuracion')
        self.audio_manager = audio_manager

        self.background_image = self.load_background_image("background_image.png")

        self.teams = self.load_teams_data()
        self.selected_team_local = 0
        self.selected_team_visit = 1

        self.selected_shooter_local = 0
        self.selected_goalie_local = 0
        self.selected_shooter_visit = 0
        self.selected_goalie_visit = 0

        self.change_mode = "auto"

        self.potentiometer_value = 0
        self.selection_mode = "Equipo local"

        self.config_complete = False

    def load_background_image(self, filename):
        image_path = os.path.join(IMAGES_DIR, filename)
        background_image = pygame.image.load(image_path)
        return pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def load_teams_data(self):
        """Carga los datos de equipos y jugadores"""
        # TODO: Modificar con tus equipos y jugadores reales
        return [
            {
                "name": "Real Madrid",
                "shield": "team2.png",
                "shooters": [
                    {"name": "Cristiano Ronaldo", "photo": "shooter1a.jpg"},
                    {"name": "Luka Modrić", "photo": "shooter2a.jpg"},
                    {"name": "Marcelo Vieira", "photo": "shooter3a.jpg"}
                ],
                "goalies": [
                    {"name": "Iker Casillas", "photo": "goalie1a.jpg"},
                    {"name": "Keylor Navas", "photo": "goalie2a.jpg"},
                    {"name": "Thibaut Courtois", "photo": "goalie3a.jpg"}
                ]
            },
            {
                "name": "Barcelona",
                "shield": "team1.png",
                "shooters": [
                    {"name": "Ronaldinho Gaúcho", "photo": "shooter1b.jpg"},
                    {"name": "Neymar", "photo": "shooter2b.jpg"},
                    {"name": "Lionel Messi", "photo": "shooter3b.jpg"}
                ],
                "goalies": [
                    {"name": "Marc-André ter Stegen", "photo": "goalie1b.jpg"},
                    {"name": "Tomasz Szczęsny", "photo": "goalie2b.jpg"},
                    {"name": "Claudio Bravo", "photo": "goalie3b.jpg"}
                ]
            },
            {
                "name": "Chelsea",
                "shield": "team3.png",
                "shooters": [
                    {"name": "N'Golo Kanté", "photo": "shooter1c.jpg"},
                    {"name": "Cole Palmer", "photo": "shooter2c.jpg"},
                    {"name": "Eden Hazard", "photo": "shooter3c.jpg"}
                ],
                "goalies": [
                    {"name": "Petr Čech", "photo": "goalie1c.jpg"},
                    {"name": "Kepa Arrizabalaga", "photo": "goalie2c.jpg"},
                    {"name": "Édouard Mendy", "photo": "goalie3c.jpg"}
                ]
            }
        ]

    def load_image(self, filename):
        image_path = os.path.join(IMAGES_DIR, filename)
        return pygame.image.load(image_path)

    def draw_team_selection(self):
        #Titulo
        title_text = title_font.render("Seleccion de Equipos", True, YELLOW)
        self.screen.blit(title_text, (SCREEN_CENTER[0] - title_text.get_width()//2, 30))

        #Equipo Local
        local_text = header_font.render("Equipo Local", True, LIGHT_BLUE)
        self.screen.blit(local_text, (SCREEN_CENTER[0] - 400, 100))

        #Equipo visitante
        visit_text = header_font.render("Equipo Visitante", True, LIGHT_BLUE)
        self.screen.blit(visit_text, (SCREEN_CENTER[0] + 200, 100))

        #Mostrar quipos seleccionados
        local_team = self.teams[self.selected_team_local]
        visit_team = self.teams[self.selected_team_visit]

        #Escudos
        local_shield = self.load_image(local_team["shield"])
        visit_shield = self.load_image(visit_team["shield"])

        if local_shield:
            local_shield = pygame.transform.scale(local_shield, (150, 150))
            self.screen.blit(local_shield, (SCREEN_CENTER[0] - 400, 150))

        if visit_shield:
            visit_shield = pygame.transform.scale(visit_shield, (150, 150))
            self.screen.blit(visit_shield, (SCREEN_CENTER[0] + 200, 150))

        #Nombres de equipos
        local_name = text_font.render(local_team["name"], True, WHITE)
        visit_name = text_font.render(visit_team["name"], True, WHITE)

        self.screen.blit(local_name, (SCREEN_CENTER[0] - 400, 320))
        self.screen.blit(visit_name, (SCREEN_CENTER[0] + 200, 320))

    def draw_player_selection(self):
        #Titulo
        title_text = title_font.render("Seleccion de Jugadores", True, YELLOW)
        self.screen.blit(title_text, (SCREEN_CENTER[0] - title_text.get_width()//2 - 5, 350))

        local_team = self.teams[self.selected_team_local]
        visit_team = self.teams[self.selected_team_visit]

        #Jugadores locales
        local_shooter = local_team["shooters"][self.selected_shooter_local]
        local_goalie = local_team["goalies"][self.selected_goalie_local]

        #Jugadores visitantes
        visit_shooter = visit_team["shooters"][self.selected_shooter_visit]
        visit_goalie = visit_team["goalies"][self.selected_goalie_visit]

        #Dibujar seccion local
        self.draw_player_section(local_shooter, local_goalie, SCREEN_CENTER[0] - 300, 450)

        #Dibujar seccion visitante
        self.draw_player_section(visit_shooter, visit_goalie, SCREEN_CENTER[0] + 100, 450)

        #Indicador de seleccion actual
        mode_text = small_font.render(f"Seleccionando: {self.selection_mode.upper()}", True, YELLOW)
        self.screen.blit(mode_text, (SCREEN_CENTER[0] - mode_text.get_width()//2, 650))

        #Instrucciones
        instr_text = small_font.render("TAB: Cambiar modo | ESPACIO: Cambiar jugador | ENTER: Continuar", True, WHITE)
        self.screen.blit(instr_text, (SCREEN_CENTER[0] - instr_text.get_width()//2, 680))

    def load_player_photo(self, filename):
        photo_path = os.path.join(IMAGES_DIR, "players", filename)
        if os.path.exists(photo_path):
            return pygame.image.load(photo_path)
        else:
            return None

    def draw_player_section(self, shooter, goalie, x ,y):
        #Artillero
        shooter_photo = self.load_player_photo(shooter["photo"])
        if shooter_photo:
            shooter_photo = pygame.transform.scale(shooter_photo, (80, 100))
            self.screen.blit(shooter_photo, (x, y - 55))

        shooter_text = text_font.render("Artillero: ", True, WHITE)
        self.screen.blit(shooter_text, (x + 90, y - 40))

        shooter_name = text_font.render(shooter["name"], True, YELLOW)
        self.screen.blit(shooter_name, (x + 90, y - 20))

        #Portero
        goalie_photo = self.load_player_photo(goalie["photo"])
        if goalie_photo:
            goalie_photo = pygame.transform.scale(goalie_photo, (80, 100))
            self.screen.blit(goalie_photo, (x, y + 80))

        goalie_text = text_font.render("Portero:", True, WHITE)
        self.screen.blit(goalie_text, (x + 95, y + 80))

        goalie_name = text_font.render(goalie["name"], True, YELLOW)
        self.screen.blit(goalie_name, (x + 95, y + 100))



    def draw_mode_selection(self):
        mode_text = header_font.render("Modo de cambio:", True, LIGHT_BLUE)
        self.screen.blit(mode_text, (SCREEN_CENTER[0] - 115, 150))

        #Boton Auto
        auto_color = GREEN if self.change_mode == "auto" else BLUE
        auto_rect = pygame.Rect(SCREEN_CENTER[0] - 120, 210, 100, 40)
        pygame.draw.rect(screen, auto_color, auto_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, auto_rect, 2, border_radius=10)

        auto_text = text_font.render("Auto", True, WHITE)
        self.screen.blit(auto_text, (auto_rect.centerx - auto_text.get_width()//2, auto_rect.centery - auto_text.get_height()//2))

        #Boton Manual
        manual_color = GREEN if self.change_mode == "manual" else BLUE
        manual_rect = pygame.Rect(SCREEN_CENTER[0] - 10, 210, 100, 40)
        pygame.draw.rect(self.screen, manual_color, manual_rect, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, manual_rect, 2, border_radius=10)

        manual_text = text_font.render("Manual", True, WHITE)
        self.screen.blit(manual_text, (manual_rect.centerx - manual_text.get_width() // 2,
                                       manual_rect.centery - manual_text.get_height() // 2))

        return auto_rect, manual_rect

    def draw_complete_button(self):
        complete_rect = pygame.Rect(SCREEN_CENTER[0] + 330, SCREEN_HEIGHT - 80, 200, 50)
        pygame.draw.rect(self.screen, GREEN, complete_rect, border_radius=15)
        pygame.draw.rect(self.screen, WHITE, complete_rect, 3, border_radius=15)

        complete_text = header_font.render("INICIAR JUEGO", True, WHITE)
        self.screen.blit(complete_text, (complete_rect.centerx - complete_text.get_width() // 2,
                                         complete_rect.centery - complete_text.get_height() // 2))

        return complete_rect

    def draw(self):
        # Fondo
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
        else:
            self.screen.fill(GREEN)

        # Dibujar componentes
        self.draw_team_selection()
        self.draw_player_selection()
        auto_rect, manual_rect = self.draw_mode_selection()
        complete_rect = self.draw_complete_button()

        pygame.display.flip()

        return auto_rect, manual_rect, complete_rect


    def handle_events(self):
        """Maneja eventos de la pantalla de configuración"""
        auto_rect, manual_rect, complete_rect = self.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
                elif event.key == pygame.K_RETURN:
                    if self.config_complete:
                        return "start_game"
                elif event.key == pygame.K_TAB:

                    # Cambiar modo de selección
                    modes = ["Equipo local", "Equipo visitante", "Tirador local", "Portero local", "Tirador visitante",
                             "Portero visitante"]
                    current_index = modes.index(self.selection_mode)
                    self.selection_mode = modes[(current_index + 1) % len(modes)]

                elif event.key == pygame.K_SPACE:
                    # Cambiar jugador seleccionado (simula potenciómetro)
                    self.cycle_selection()

                elif event.key == pygame.K_UP:
                    # Cambiar equipos
                    if self.selection_mode == "Equipo local":
                        self.selected_team_local = (self.selected_team_local - 1) % len(self.teams)
                        if self.selected_team_local == self.selected_team_visit:
                            self.selected_team_local = (self.selected_team_local - 1) % len(self.teams)
                    elif self.selection_mode == "Equipo visitante":
                        self.selected_team_visit = (self.selected_team_visit - 1) % len(self.teams)
                        if self.selected_team_visit == self.selected_team_local:
                            self.selected_team_visit = (self.selected_team_visit - 1) % len(self.teams)

                elif event.key == pygame.K_DOWN:
                    # Cambiar equipos
                    if self.selection_mode == "Equipo local":
                        self.selected_team_local = (self.selected_team_local + 1) % len(self.teams)
                        if self.selected_team_local == self.selected_team_visit:
                            self.selected_team_local = (self.selected_team_local + 1) % len(self.teams)
                    elif self.selection_mode == "Equipo visitante":
                        self.selected_team_visit = (self.selected_team_visit + 1) % len(self.teams)
                        if self.selected_team_visit == self.selected_team_local:
                            self.selected_team_visit = (self.selected_team_visit + 1) % len(self.teams)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Modo de cambio
                if auto_rect.collidepoint(mouse_pos):
                    self.change_mode = "auto"
                elif manual_rect.collidepoint(mouse_pos):
                    self.change_mode = "manual"
                elif complete_rect.collidepoint(mouse_pos):
                    if self.validate_configuration():
                        self.config_complete = True
                        return "start_game"

        return "config"

    def cycle_selection(self):
        """Cicla entre las opciones del modo de selección actual"""
        if self.selection_mode == "Tirador local":
            self.selected_shooter_local = (self.selected_shooter_local + 1) % 3
        elif self.selection_mode == "Portero local":
            self.selected_goalie_local = (self.selected_goalie_local + 1) % 3
        elif self.selection_mode == "Tirador visitante":
            self.selected_shooter_visit = (self.selected_shooter_visit + 1) % 3
        elif self.selection_mode == "Portero visitante":
            self.selected_goalie_visit = (self.selected_goalie_visit + 1) % 3

    def validate_configuration(self):
        #Verificar que los equipos sean diferentes
        if self.selected_team_local == self.selected_team_visit:
            print("ERROR, los equipos debens ser diferentes")
            return False

        return True

    def get_configuration(self):
        #Retorna la configuracion seleccionada

        return {"team_local": self.teams[self.selected_team_local],
                "team_visit": self.teams[self.selected_team_visit],
                "shooter_local": self.selected_shooter_local,
                "shooter_visit": self.selected_shooter_visit,
                "goalie_local": self.selected_goalie_local,
                "goalie_visit": self.selected_goalie_visit,
                "change_mode": self.change_mode}

    def run(self):
        while self.running:
            action = self.handle_events()
            if action != "config":
                return action, self.get_configuration() if action == "start_game" else None

            self.draw()
            pygame.time.Clock().tick(60)