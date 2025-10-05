import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

#Instrucciones del juego
INSTRUCTIONS = [
    "INSTRUCCIONES DE USO - Jonathaninho Soccer 64 v1.0",
    "",
    "CONFIGURACIÓN INICIAL:",
    "• Use el potenciómetro para seleccionar jugadores",
    "• Elija entre modo Manual o Automático",
    "• Seleccione artillero y portero para cada equipo",
    "",
    "DURANTE EL JUEGO:",
    "• Cada equipo realiza 5 tiros alternados",
    "• Tiene 3 segundos para cobrar después del silbato",
    "• Modo automático: cambio cada 5 segundos",
    "• Modo manual: cambio con botón físico",
    "",
    "PUNTAJE:",
    "• Gol válido: pelota pasa por paleta no cubierta",
    "• Gol anulado: portero cubre la paleta",
    "• Tiro fallado: se agota el tiempo",
    "",
    "CONTROLES FÍSICOS:",
    "• Potenciómetro: selección de jugadores",
    "• Botón: cambio manual de jugador",
    "• Paletas: detección de dirección del tiro",
    "",
    "SONIDOS:",
    "• Silbato: inicio de turno",
    "• Porras: gol anotado",
    "• Abucheos: gol anulado",
    "",
    "¡Disfrute del juego!"
]



class InstructionsScreen:
    def __init__(self):
        self.running = True
        self.scroll_offset = 0
        self.max_scroll = 400
        self.breath_alpha = BREATH_MIN_ALPHA
        self.breath_direction = 1

    def update_breath_effect(self):
        """Actualiza el efecto de respiración"""
        self.breath_alpha += BREATH_SPEED * self.breath_direction
        if self.breath_alpha >= BREATH_MAX_ALPHA:
            self.breath_alpha = BREATH_MAX_ALPHA
            self.breath_direction = -1
        elif self.breath_alpha <= BREATH_MIN_ALPHA:
            self.breath_alpha = BREATH_MIN_ALPHA
            self.breath_direction = 1

    def draw_help_text_with_breath(self, text, font, color, x, y):
        """Dibuja texto con efecto de respiración"""
        text_surface = font.render(text, True, color)
        text_surface.set_alpha(self.breath_alpha)
        screen.blit(text_surface, (x, y))

    def draw_back_button(self):
        """Dibuja el botón para regresar a la pantalla Acerca de"""
        back_rect = pygame.Rect(50, 30, 120, 40)
        pygame.draw.rect(screen, BUTTON_COLOR, back_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), back_rect, 2, border_radius=10)

        back_text = text_font.render("Atrás", True, (255, 255, 255))
        screen.blit(back_text, (back_rect.x + 20, back_rect.y + 8))

        return back_rect

    def draw_scroll_indicator(self):
        """Dibuja un indicador de scroll"""
        if self.max_scroll > 0:
            scroll_ratio = self.scroll_offset / self.max_scroll
            scrollbar_height = 100
            scrollbar_y = 50 + (SCREEN_HEIGHT - 150) * scroll_ratio

            pygame.draw.rect(screen, (200, 200, 200), (SCREEN_WIDTH - 20, 50, 10, SCREEN_HEIGHT - 100), 2)
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, (SCREEN_WIDTH - 20, scrollbar_y, 10, scrollbar_height))

    def draw(self):
        """Dibuja la pantalla de instrucciones"""
        #Actualizar efecto de respiracion
        self.update_breath_effect()

        # Fondo
        screen.fill(BACKGROUND_COLOR)

        # Botón regresar
        back_rect = self.draw_back_button()

        # Título
        title_text = title_font.render("Instrucciones del Juego", True, TITLE_COLOR)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 20))

        # Aplicar scroll offset
        base_y = 100 - self.scroll_offset

        # Instrucciones
        for i, line in enumerate(INSTRUCTIONS):
            if line == "":
                base_y += 10  # Espacio extra para líneas vacías
                continue

            if line.startswith("INSTRUCCIONES"):
                text_surface = header_font.render(line, True, HIGHLIGHT_COLOR)
            elif line.endswith(":"):
                text_surface = text_font.render(line, True, HIGHLIGHT_COLOR)
            else:
                text_surface = small_font.render(line, True, TEXT_COLOR)

            screen.blit(text_surface, (50, base_y))
            base_y += 30

        # Actualizar max_scroll basado en el contenido real
        content_height = base_y + self.scroll_offset - 100
        self.max_scroll = max(0, content_height - (SCREEN_HEIGHT - 150))

        # Indicador de scroll
        self.draw_scroll_indicator()

        # Mensaje de navegación
        nav_text = "Use la rueda del mouse o las teclas de flecha para bajar/subir la pantalla"
        nav_x = SCREEN_WIDTH // 2 - small_font.size(nav_text)[0] // 2
        self.draw_help_text_with_breath(nav_text, small_font, (200, 200, 200), nav_x, SCREEN_HEIGHT - 50)
        pygame.display.flip()

    def handle_events(self):
        """Maneja los eventos de la pantalla de instrucciones"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "quit"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
                # Navegación con teclado
                elif event.key == pygame.K_DOWN:
                    self.scroll_offset = min(self.scroll_offset + 30, self.max_scroll)
                elif event.key == pygame.K_UP:
                    self.scroll_offset = max(self.scroll_offset - 30, 0)

            elif event.type == pygame.MOUSEWHEEL:
                # Scroll con rueda del mouse
                self.scroll_offset = max(0, min(self.scroll_offset - event.y * 30, self.max_scroll))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                back_rect = pygame.Rect(50, 30, 120, 40)
                if back_rect.collidepoint(mouse_pos):
                    return "back"

        return "instructions"

    def run(self):
        """Ejecuta la pantalla de instrucciones"""
        while self.running:
            action = self.handle_events()
            if action != "instructions":
                return action

            self.draw()
            pygame.time.Clock().tick(60)