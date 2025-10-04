import pygame
import sys
import os

pygame.init()

GREEN = 15, 30, 15
YELLOW = 220, 220, 0
WHITE = 255, 255, 255
LIGHT_BLUE = 0, 200, 255

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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
#FONTS_DIR = os.path.join(BASE_DIR, "fonts")

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
    def __init__(self):
        self.running = True
        self.scroll_offset = 0
        self.max_scroll = 400

        self.title_image = self.load_image(PROJECT_INFO["title_image"])
        if self.title_image:
            # Escalar la imagen del título si es necesario
            original_width, original_height = self.title_image.get_size()
            new_width = 500  # Ancho deseado
            new_height = int(original_height * (new_width / original_width))
            self.title_image = pygame.transform.scale(self.title_image, (new_width, new_height))

    def load_image(self, filename):
        """Carga una imagen desde la carpeta images"""
        try:
            image_path = os.path.join(IMAGES_DIR, filename)
            if os.path.exists(image_path):
                return pygame.image.load(image_path)
            else:
                print(f"Archivo no encontrado: {image_path}")
                return None
        except pygame.error as e:
            print(f"Error cargando imagen {filename}: {e}")
            return None

    def draw_author_photo(self, x, y, photo_filename, author_name):
        photo_path = os.path.join(IMAGES_DIR, photo_filename)
        photo = pygame.image.load(photo_path)
        photo = pygame.transform.scale(photo, (120, 150))
        screen.blit(photo, (x, y))

        pygame.draw.rect(screen, HIGHLIGHT_COLOR, (x - 5, y - 5, 130, 160), 2)

        name_text = small_font.render(author_name, True, TEXT_COLOR)
        screen.blit(name_text, (x - 10, y + 160))

    def draw_back_button(self):
        back_rect = pygame.Rect(50, 30, 120, 40)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, back_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), back_rect, 2, border_radius=10)

        back_text = text_font.render("← Regresar", True, (255, 255, 255))
        screen.blit(back_text, (back_rect.x + 10, back_rect.y + 8))

        return back_rect

    def draw(self):
        """Dibuja toda la pantalla Acerca de"""
        # Fondo
        screen.fill(BACKGROUND_COLOR)

        # Botón regresar
        back_rect = self.draw_back_button()

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
            screen.blit(id_text, (x_pos - 10, y_offset + 180))

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
        y_offset += 20
        help_text = small_font.render("Presione ESC o haga clic en 'Regresar' para volver al menú principal", True,
                                      (200, 200, 200))
        screen.blit(help_text, (SCREEN_WIDTH // 2 - help_text.get_width() // 2, SCREEN_HEIGHT - 25))

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
                if back_rect.collidepoint(mouse_pos):
                    return "back"

        return "about"

    def run(self):
        """Ejecuta la pantalla Acerca de"""
        while self.running:
            action = self.handle_events()
            if action != "about":
                return action

            self.draw()
            pygame.time.Clock().tick(60)

# Función principal para probar la pantalla
def main():
    about_screen = AboutScreen()
    result = about_screen.run()

    if result == "quit":
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()