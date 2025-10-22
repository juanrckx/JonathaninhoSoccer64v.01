import pygame
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *


class StatsScreen:
    def __init__(self, stats_manager, audio_manager=None):
        self.running = True
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Jonathaninho Soccer 64 - Estadísticas')
        self.audio_manager = audio_manager
        self.background_image = self.load_image("background_image.png")
        self.stats_manager = stats_manager

        # Navegación entre pestañas
        self.current_tab = "overview"  # overview, players, teams, games
        self.sort_by = "goals"  # Para jugadores: goals, accuracy, games

    def load_image(self, filename):
        image_path = os.path.join(IMAGES_DIR, filename)
        return pygame.image.load(image_path)

    def draw_tabs(self):
        """Dibuja las pestañas de navegación"""
        tabs = [
            ("Resumen", "overview"),
            ("Jugadores", "players"),
            ("Equipos", "teams"),
            ("Partidos", "games")
        ]

        tab_width = SCREEN_WIDTH // len(tabs)
        tab_rects = []

        for i, (label, tab_id) in enumerate(tabs):
            tab_x = i * tab_width
            color = GREEN if self.current_tab == tab_id else BLUE
            tab_rect = pygame.Rect(tab_x, 80, tab_width, 40)

            pygame.draw.rect(self.screen, color, tab_rect)
            pygame.draw.rect(self.screen, WHITE, tab_rect, 2)

            tab_text = text_font.render(label, True, WHITE)
            self.screen.blit(tab_text, (tab_x + tab_width // 2 - tab_text.get_width() // 2, 95))

            tab_rects.append((tab_rect, tab_id))

        return tab_rects

    def draw_overview(self):
        """Dibuja la pestaña de resumen general"""
        stats = self.stats_manager.stats
        y_pos = 150

        # Título
        title_text = title_font.render("ESTADÍSTICAS GENERALES", True, YELLOW)
        self.screen.blit(title_text, (SCREEN_CENTER[0] - title_text.get_width() // 2, 120))

        # Estadísticas principales
        main_stats = [
            f"Total de Partidos: {stats['total_games']}",
            f"Total de Goles: {stats['total_goals']}",
            f"Promedio de Goles por Partido: {stats['total_goals'] / max(stats['total_games'], 1):.1f}",
            f"Récord de Goles en un Partido: {stats['records']['most_goals_game']}",
            f"Mejor Precisión: {stats['records']['best_accuracy']:.1f}%"
        ]

        for stat in main_stats:
            stat_text = header_font.render(stat, True, WHITE)
            self.screen.blit(stat_text, (SCREEN_CENTER[0] - stat_text.get_width() // 2, y_pos))
            y_pos += 40

        # Top jugadores
        y_pos += 30
        top_title = header_font.render("MÁXIMOS GOLEADORES", True, LIGHT_BLUE)
        self.screen.blit(top_title, (SCREEN_CENTER[0] - top_title.get_width() // 2, y_pos))
        y_pos += 40

        top_scorers = self.stats_manager.get_top_scorers(3)
        for i, (name, data) in enumerate(top_scorers):
            accuracy = (data["goals"] / max(data["shots"], 1)) * 100
            scorer_text = text_font.render(
                f"{i + 1}. {name}: {data['goals']} goles, {accuracy:.1f}% precisión",
                True, WHITE
            )
            self.screen.blit(scorer_text, (SCREEN_CENTER[0] - scorer_text.get_width() // 2, y_pos))
            y_pos += 30

    def draw_players_tab(self):
        """Dibuja la pestaña de estadísticas de jugadores"""
        y_pos = 150

        # Título y controles de ordenamiento
        title_text = title_font.render("ESTADÍSTICAS DE JUGADORES", True, YELLOW)
        self.screen.blit(title_text, (SCREEN_CENTER[0] - title_text.get_width() // 2, 120))

        # Botones de ordenamiento
        sort_options = [("Goles", "goals"), ("Precisión", "accuracy"), ("Partidos", "games")]
        sort_rects = []
        x_pos = SCREEN_CENTER[0] - 150

        for i, (label, sort_type) in enumerate(sort_options):
            color = GREEN if self.sort_by == sort_type else BLUE
            sort_rect = pygame.Rect(x_pos + i * 100, y_pos, 90, 30)
            pygame.draw.rect(self.screen, color, sort_rect, border_radius=5)
            pygame.draw.rect(self.screen, WHITE, sort_rect, 2, border_radius=5)

            sort_text = small_font.render(label, True, WHITE)
            self.screen.blit(sort_text, (sort_rect.centerx - sort_text.get_width() // 2,
                                         sort_rect.centery - sort_text.get_height() // 2))
            sort_rects.append((sort_rect, sort_type))

        y_pos += 50

        # Lista de jugadores
        shooters = {name: data for name, data in self.stats_manager.stats["players"].items() if
                    data["role"] == "shooter"}

        # Ordenar jugadores
        if self.sort_by == "goals":
            sorted_players = sorted(shooters.items(), key=lambda x: x[1]["goals"], reverse=True)
        elif self.sort_by == "accuracy":
            sorted_players = sorted(shooters.items(),
                                    key=lambda x: (x[1]["goals"] / max(x[1]["shots"], 1)) * 100,
                                    reverse=True)
        else:  # games
            sorted_players = sorted(shooters.items(), key=lambda x: x[1]["games"], reverse=True)

        # Encabezados de tabla
        headers = ["Jugador", "Equipo", "Part", "Goles", "Tiros", "Prec%", "Timeouts"]
        header_x = [50, 250, 350, 420, 490, 560, 650]

        for i, header in enumerate(headers):
            header_text = text_font.render(header, True, LIGHT_BLUE)
            self.screen.blit(header_text, (header_x[i], y_pos))

        y_pos += 30

        # Datos de jugadores
        for name, data in sorted_players[:15]:  # Mostrar primeros 15
            accuracy = (data["goals"] / max(data["shots"], 1)) * 100
            player_data = [
                name,
                data["team"],
                str(data["games"]),
                str(data["goals"]),
                str(data["shots"]),
                f"{accuracy:.1f}%",
                str(data.get("timeouts", 0))
            ]

            for i, value in enumerate(player_data):
                value_text = small_font.render(value, True, WHITE)
                self.screen.blit(value_text, (header_x[i], y_pos))

            y_pos += 25

        return sort_rects

    def draw_teams_tab(self):
        """Dibuja la pestaña de estadísticas de equipos"""
        y_pos = 150

        title_text = title_font.render("ESTADÍSTICAS DE EQUIPOS", True, YELLOW)
        self.screen.blit(title_text, (SCREEN_CENTER[0] - title_text.get_width() // 2, 120))

        # Encabezados de tabla
        headers = ["Equipo", "Part", "G", "E", "P", "GF", "GC", "DG", "Efect%"]
        header_x = [50, 200, 250, 290, 330, 370, 420, 470, 520]

        for i, header in enumerate(headers):
            header_text = text_font.render(header, True, LIGHT_BLUE)
            self.screen.blit(header_text, (header_x[i], y_pos))

        y_pos += 30

        # Datos de equipos
        for team_name, data in self.stats_manager.stats["teams"].items():
            goal_diff = data["goals_for"] - data["goals_against"]
            effectiveness = (data["wins"] / max(data["games"], 1)) * 100

            team_data = [
                team_name,
                str(data["games"]),
                str(data["wins"]),
                str(data["draws"]),
                str(data["losses"]),
                str(data["goals_for"]),
                str(data["goals_against"]),
                f"{goal_diff:+d}",
                f"{effectiveness:.1f}%"
            ]

            for i, value in enumerate(team_data):
                value_text = small_font.render(value, True, WHITE)
                self.screen.blit(value_text, (header_x[i], y_pos))

            y_pos += 25

    def draw_games_tab(self):
        """Dibuja la pestaña de historial de partidos"""
        y_pos = 150

        title_text = title_font.render("HISTORIAL DE PARTIDOS", True, YELLOW)
        self.screen.blit(title_text, (SCREEN_CENTER[0] - title_text.get_width() // 2, 120))

        # Encabezados
        headers = ["Fecha", "Local", "Resultado", "Visitante"]
        header_x = [50, 200, 400, 500]

        for i, header in enumerate(headers):
            header_text = text_font.render(header, True, LIGHT_BLUE)
            self.screen.blit(header_text, (header_x[i], y_pos))

        y_pos += 30

        # Partidos recientes (últimos 10)
        recent_games = self.stats_manager.get_recent_games(10)

        for game in reversed(recent_games):
            local_team = game["config"]["team_local"]["name"]
            visit_team = game["config"]["team_visit"]["name"]
            score = f"{game['score']['local']} - {game['score']['visit']}"

            # Formatear fecha
            game_date = datetime.fromisoformat(game["timestamp"]).strftime("%d/%m %H:%M")

            game_data = [game_date, local_team, score, visit_team]

            for i, value in enumerate(game_data):
                value_text = small_font.render(value, True, WHITE)
                self.screen.blit(value_text, (header_x[i], y_pos))

            y_pos += 25

    def draw(self):
        """Dibuja toda la pantalla de estadísticas"""
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
        else:
            self.screen.fill(BACKGROUND_COLOR)

        # Pestañas
        tab_rects = self.draw_tabs()

        # Contenido según pestaña activa
        sort_rects = []
        if self.current_tab == "overview":
            self.draw_overview()
        elif self.current_tab == "players":
            sort_rects = self.draw_players_tab()
        elif self.current_tab == "teams":
            self.draw_teams_tab()
        elif self.current_tab == "games":
            self.draw_games_tab()

        # Instrucciones
        instr_text = small_font.render("Presione ESC para volver al menú principal", True, WHITE)
        self.screen.blit(instr_text, (SCREEN_CENTER[0] - instr_text.get_width() // 2, SCREEN_HEIGHT - 50))

        pygame.display.flip()
        return tab_rects, sort_rects

    def handle_events(self):
        """Maneja eventos de la pantalla de estadísticas"""
        tab_rects, sort_rects = self.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Verificar clics en pestañas
                for rect, tab_id in tab_rects:
                    if rect.collidepoint(mouse_pos):
                        self.current_tab = tab_id

                # Verificar clics en ordenamiento (solo en pestaña de jugadores)
                if self.current_tab == "players":
                    for rect, sort_type in sort_rects:
                        if rect.collidepoint(mouse_pos):
                            self.sort_by = sort_type

        return "stats"

    def run(self):
        """Ejecuta la pantalla de estadísticas"""
        while self.running:
            action = self.handle_events()
            if action != "stats":
                return action

            pygame.time.Clock().tick(60)
        return None