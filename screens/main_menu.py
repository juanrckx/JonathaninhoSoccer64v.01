import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class MainMenu:
    def __init__(self, audio_manager=None):
        self.running = True
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jonathaninho Soccer 64 - Pantalla principal")

        self.audio_manager = audio_manager

        self.title_image = self.load_image("title_image.png")
        self.background_image = self.load_image("background_image.png")

        self.button_glow = 0
        self.glow_direction = 1


    def load_sound(self, file_name):
        """Carga la musica de fondo"""
        sound_path = os.path.join(SOUNDS_DIR, file_name)
        return pygame.mixer.Sound(file_name)

    def load_image(self, file_name):
        """Carga la imagen de fondo"""
        image_path = os.path.join(IMAGES_DIR, file_name)
        return pygame.image.load(image_path)

    def draw_glowing_button(self, text, rect, base_color, glow_color):
        glow_intensity = abs(pygame.time.get_ticks() % 2000 - 1000) / 1000
        current_glow = [int(base_color[i] + (glow_color[i] - base_color[i]) * glow_intensity) for i in range(3)]

        pygame.draw.rect(self.screen, current_glow, rect, border_radius=15)
        pygame.draw.rect(self.screen, WHITE, rect, 3, border_radius=15)

        # Texto del botón
        text_surface = text_font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

        return rect

    def draw(self):
        """Dibuja el menú principal"""
        # Fondo con imagen
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))

            # Capa semi-transparente para mejorar legibilidad del texto
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Negro semi-transparente (alpha = 128/255)
            self.screen.blit(overlay, (0, 0))
        else:
            # Fallback: fondo verde sólido si no hay imagen
            self.screen.fill(GREEN)

        # Logo/Título
        if self.title_image:
            title_rect = self.title_image.get_rect(center=(SCREEN_CENTER[0], 150))
            self.screen.blit(self.title_image, title_rect)
        else:
            title_text = title_font.render("Jonathaninho Soccer 64", True, YELLOW)
            title_rect = title_text.get_rect(center=(SCREEN_CENTER[0], 150))
            self.screen.blit(title_text, title_rect)

        # Botones
        button_width, button_height = 300, 60
        button_y_start = 350
        button_spacing = 80

        buttons = [
            {"text": "Nueva Partida", "action": "new_game", "rect": pygame.Rect(0, 0, button_width, button_height)},
            {"text": "Acerca de", "action": "about", "rect": pygame.Rect(0, 0, button_width, button_height)},
            {"text": "Salir", "action": "quit", "rect": pygame.Rect(0, 0, button_width, button_height)}
        ]

        # Posicionar botones
        for i, button in enumerate(buttons):
            button["rect"].center = ((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)[0], button_y_start + i * button_spacing)

        # Dibujar botones y detectar hover
        mouse_pos = pygame.mouse.get_pos()
        hovered_action = None

        for button in buttons:
            color = LIGHT_BLUE if button["rect"].collidepoint(mouse_pos) else BLUE
            glow_color = YELLOW if button["rect"].collidepoint(mouse_pos) else WHITE

            drawn_rect = self.draw_glowing_button(button["text"], button["rect"], color, glow_color)
            button["drawn_rect"] = drawn_rect

            if drawn_rect.collidepoint(mouse_pos):
                hovered_action = button["action"]

        # Texto de ayuda
        help_text = small_font.render("Seleccione una opción con el mouse", True, (200, 200, 200))
        help_rect = help_text.get_rect(center=((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)[0], SCREEN_HEIGHT - 50))
        self.screen.blit(help_text, help_rect)

        pygame.display.flip()
        return buttons, hovered_action

    def handle_events(self):
        """Maneja eventos del menú principal"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    buttons, hovered_action = self.draw()  # Redibujar para obtener botones actualizados
                    mouse_pos = pygame.mouse.get_pos()

                    for button in buttons:
                        if button["drawn_rect"].collidepoint(mouse_pos):
                            return button["action"]

        return "main_menu"

    def run(self):
        """Ejecuta el menú principal"""

        while self.running:
            action = self.handle_events()

            if action != "main_menu":
                return action


            self.draw()
            pygame.time.Clock().tick(60)
        return None