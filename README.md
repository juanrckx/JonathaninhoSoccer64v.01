JONATHANINHO SOCCER 64 es un sistema interactivo de futbolín de tipo penalties que combina una maqueta física con un videojuego en Python, desarrollado como proyecto académico para el curso CE-1104 Fundamentos de Sistemas Computacionales.

Características Principales:
- Juego de penalties con 5 tiros por equipo
- Dos modos de juego: Automático y Manual
- Sistema de estadísticas completo con persistencia
- Efectos de sonido inmersivos (porras, silbato, abucheos)
- Comunicación inalámbrica con maqueta física
- Interfaz gráfica moderna desarrollada con Pygame

Para el proyecto se utiliza:
- Lenguaje: Python 3.9+
- Librerias: Pygame, JSON.
- Plataforma: Windows/Linux/macOS

Hardware:
-Microcontrolador: Raspberry Pi Pico W
-Componentes: 6 paletas, 2 botones, 1 potenciómetro
- Indicadores de 6 LEDs de paletas
- Comunicacion a través de WiFi 2.4GHz

Instalación y Configuración:
bash:
- Python 3.9 o superior
- pip install pygame

bash:
- git clone https://github.com/tu-usuario/JonathaninhoSoccer64v.01.git
- cd Jonathaninho Soccer 64

bash:
- pip install -r requirements.txt

- Conectar Raspberry Pi Pico W según diagrama de pines
- Cargar firmware en el Pico W
- Verificar conexión WiFi

Cómo jugar:
1. Menú Principal → Seleccionar "Nueva Partida"
2. Configuración → Elegir equipos y jugadores
3. Sorteo → Lanzamiento de moneda para local/visitante
4. Juego → 5 tiros alternados por equipo
5. Resultados → Ver estadísticas y ganador

- Controles (teclado):
1. Teclas 1-6: Disparar a paletas correspondientes
2. ESPACIO: Continuar/Confirmar
3. ESC: Volver al menú
4. TAB: Cambiar modo de selección

Configuración Hardware:
- POTENCIÓMETRO → GPIO 26 (ADC)
- BOTÓN 1 → GPIO 15
- BOTÓN 2 → GPIO 14  
- PALETA 0 → GPIO 1
- PALETA 1 → GPIO 2
- PALETA 2 → GPIO 3
- PALETA 3 → GPIO 4
- PALETA 4 → GPIO 5
- PALETA 5 → GPIO 6
- LED 0 → GPIO 8
- LED 1 → GPIO 9
- LED 2 → GPIO 10
- LED 3 → GPIO 11
- LED 4 → GPIO 12
- LED 5 → GPIO 13

Estructura:
- JonathaninhoSoccer64v1.0/
- ├── screens/                 # Pantallas de la aplicación
- │   ├── main_menu.py           # Menú principal
- │   ├── about_screen.py        # Acerca del proyecto
- │   ├── config_screen.py       # Configuración de partida
- │   ├── game_screen.py         # Juego principal
- │   ├── coin_toss_screen.py    # Sorteo de moneda
- │   ├── stats_screen.py        # Estadísticas
- │   ├── stats_manager.py       # Gestor de estadísticas
- │   └── instructions_screen.py # Instrucciones
- ├── images/                 # Recursos gráficos
- │   ├── title_image.png
- │   ├── background_image.png
- │   ├── author1.jpg, author2.jpg
- │   ├── team1.png, team2.png, team3.png
- │   └── players/           # Fotos de jugadores
- ├── sounds/                # Efectos de sonido
- │   ├── background_music.mp3
- │   ├── game_music.mp3
- │   ├── whistle.mp3
- │   ├── cheer.mp3
- │   └── boo.mp3
- ├── hardware/              # Código para Pico W
- │   └── main(raspberry).py       # Firmware principal
- ├── config.py                # Configuración global
- ├── main.py                  # Aplicación principal
- └── README.md               # Este archivo

Configuración WiFi:
- Editar:
WIFI_SSID = "tu-red-wifi"
WIFI_PASSWORD = "tu-contraseña"
SERVER_PORT = 1717

Desarrollo y Contribuciones
- Desarrolladores:
Juan Jose Rodriguez - 2025094370
Gabriel Brenes - 2025119612


- Curso:
CE-1104 Fundamentos de Sistemas Computacionales
Instituto Tecnológico de Costa Rica
2025

- Profesor:
Luis Alonso Barboza Artavia

Contribuir:
- Fork del proyecto
- Crear rama feature (git checkout -b feature/AmazingFeature)
- Commit cambios (git commit -m 'Add AmazingFeature')
- Push a la rama (git push origin feature/AmazingFeature)
- Abrir Pull Request

<img width="1606" height="1116" alt="image" src="https://github.com/user-attachments/assets/6a75fad4-86a9-417e-8e5f-08782ada4c5a" />
<img width="1610" height="1060" alt="image" src="https://github.com/user-attachments/assets/da39559b-7279-4401-be6f-7dbb4f73937c" />



