import sys
from config import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



#Informacion del proyecto
PROJECT_INFO = {"title_image": "title_image.png",
                "authors": [{"name": "Juan Jose Rodriguez ",
                             "carnet": "2025094370",
                             "photo": "author1.jpg"},
                            {"name": "Gabriel Brenes ",
                             "carnet": "2025119612",
                             "photo": "author2.jpg"}],
                "course": "CE-1104 Fundamentos de Sistemas Computacionales",
                "career": "Ingeniería en Computadores",
                "year": "2025",
                "professor": "Luis Alonso Barboza Artavia",
                "country": "Costa Rica",
                "version": "v1.0",}

class AboutScreen:
    def __init__(self, audio_manager=None):
        self.running = True
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.title_image = self.load_image(PROJECT_INFO["title_image"])
        self.background_image = self.load_image("background_image.png")

        self.audio_manager = audio_manager


        # Escalar la imagen del título si es necesario
        original_width, original_height = self.title_image.get_size()
        new_width = 500  # Ancho deseado
        new_height = int(original_height * (new_width / original_width))
        self.title_image = pygame.transform.scale(self.title_image, (new_width, new_height))

        self.breath_alpha = BREATH_MIN_ALPHA
        self.breath_direction = 1

    def update_breath(self):
        self.breath_alpha += BREATH_SPEED * self.breath_direction

        # Cambiar dirección cuando llegue a los límites
        if self.breath_alpha >= BREATH_MAX_ALPHA:
            self.breath_alpha = BREATH_MAX_ALPHA
            self.breath_direction = -1
        elif self.breath_alpha <= BREATH_MIN_ALPHA:
            self.breath_alpha = BREATH_MIN_ALPHA
            self.breath_direction = 1

    def draw_help_text_with_breath(self, text, font, color, x, y):
        """Dibuja texto con efecto de respiración"""
        # Crear una superficie temporal para el texto
        text_surface = font.render(text, True, color)

        # Aplicar alpha al texto
        text_surface.set_alpha(self.breath_alpha)
        screen.blit(text_surface, (x, y))

    def load_image(self, filename):
        """Carga una imagen desde la carpeta images"""
        image_path = os.path.join(IMAGES_DIR, filename)
        return pygame.image.load(image_path)

    def load_background_image(self):
        """Carga la imagen de fondo"""
        image_path = os.path.join(IMAGES_DIR, "background_image.png")
        return pygame.image.load(image_path)

    def draw_author_photo(self, x, y, photo_filename, author_name):
        photo_path = os.path.join(IMAGES_DIR, photo_filename)
        photo = pygame.image.load(photo_path)
        photo = pygame.transform.scale(photo, (120, 150))
        screen.blit(photo, (x, y))

        pygame.draw.rect(screen, HIGHLIGHT_COLOR, (x - 5, y - 5, 130, 160), 2)

        name_text = small_font.render(author_name, True, TEXT_COLOR)
        screen.blit(name_text, (x - 10, y + 160))

    def draw_back_button(self):
        back_rect = pygame.Rect(50, 30, 105, 40)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, back_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, back_rect, 2, border_radius=10)

        back_text = text_font.render("Regresar", True, WHITE)
        screen.blit(back_text, (back_rect.x + 10, back_rect.y + 10))

        return back_rect

    def draw_instructions_button(self):
        instructions_rect = pygame.Rect(SCREEN_WIDTH - 170, 30, 145, 40)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, instructions_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, instructions_rect, 2, border_radius=10)

        instructions_text = text_font.render("Instrucciones", True, WHITE)
        screen.blit(instructions_text, (instructions_rect.x + 10, instructions_rect.y + 10))

        return instructions_rect

    def draw(self):
        """Dibuja toda la pantalla Acerca de"""

        #Actualizar efecto de respiracion
        self.update_breath()
        # Fondo
        self.screen.blit(self.background_image, (0, 0))

        # Capa semi-transparente para mejorar legibilidad del texto
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Negro semi-transparente (alpha = 128/255)
        screen.blit(overlay, (0, 0))
        # Botones
        back_rect = self.draw_back_button()
        instructions_rect = self.draw_instructions_button()

        # Título principal (imagen)
        if self.title_image:
            title_x = SCREEN_WIDTH // 2 - self.title_image.get_width() // 2
            title_y = -25
            screen.blit(self.title_image, (title_x, title_y))
            y_offset = 225 # Espacio después del título
        else:
            # Fallback: usar texto si no hay imagen
            title_text = title_font.render(PROJECT_INFO["title"], True, TITLE_COLOR)
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 20))
            y_offset = 100

        # Información de autores
        authors_header = header_font.render("Desarrollado por:", True, HIGHLIGHT_COLOR)
        screen.blit(authors_header, (SCREEN_WIDTH // 2 - authors_header.get_width() // 2, y_offset))
        y_offset += 35

        # Fotos de autores
        author1_x = SCREEN_WIDTH // 2 - 150
        author2_x = SCREEN_WIDTH // 2 + 30

        for i, author in enumerate(PROJECT_INFO["authors"]):
            x_pos = author1_x if i == 0 else author2_x
            self.draw_author_photo(x_pos, y_offset, author["photo"], author["name"])

            # Información de identificación debajo del nombre
            id_text = small_font.render(f"Carnet: {author['carnet']}", True, TEXT_COLOR)
            self.screen.blit(id_text, (x_pos - 10, y_offset + 180))

        y_offset += 200

        # Información académica
        info_lines = [
            f"Curso: {PROJECT_INFO['course']}",
            f"Carrera: {PROJECT_INFO['career']}",
            f"Año: {PROJECT_INFO['year']}",
            f"Profesor: {PROJECT_INFO['professor']}",
            f"País: {PROJECT_INFO['country']}",
            f"Versión: {PROJECT_INFO['version']}",
        ]

        for line in info_lines:
            info_text = text_font.render(line, True, TEXT_COLOR)
            screen.blit(info_text, (SCREEN_WIDTH // 2 - info_text.get_width() // 2, y_offset))
            y_offset += 35

        # Mensaje de ayuda
        help_text = "Para instrucciones detalladas, presione el botón 'Instrucciones'"
        help_x = SCREEN_WIDTH // 2 - small_font.size(help_text)[0] // 2
        self.draw_help_text_with_breath(help_text, small_font, TEXT_COLOR, help_x, y_offset + 20)


        # Mensaje de navegación
        nav_text = "Presione ESC o haga clic en 'Regresar' para volver al menú principal"
        nav_x = SCREEN_WIDTH // 2 - small_font.size(nav_text)[0] // 2
        self.draw_help_text_with_breath(nav_text, small_font, (200, 200, 200), nav_x, SCREEN_HEIGHT - 50)

        pygame.display.flip()

    def handle_events(self):
        """Maneja los eventos de la pantalla"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "quit"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                back_rect = pygame.Rect(50, 30, 120, 40)
                instructions_rect = pygame.Rect(SCREEN_WIDTH - 170, 30, 120, 40)
                if back_rect.collidepoint(mouse_pos):
                    return "back"
                elif instructions_rect.collidepoint(mouse_pos):
                    return "instructions"

        return "about"

    def run(self):
        """Ejecuta la pantalla Acerca de"""
        while self.running:
            action = self.handle_events()
            if action != "about":
                return action

            self.draw()
            pygame.time.Clock().tick(60)