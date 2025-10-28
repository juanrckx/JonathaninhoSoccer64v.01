# proyecto fsc.py
import network
import socket
import time
from machine import Pin, ADC
import _thread
import uselect

# ==================== CONFIGURACIÓN ====================
WIFI_SSID = "Casa4"
WIFI_PASSWORD = "cartago04"
SERVER_PORT = 1717

POT_PIN = 26
BTN_PINS = [15, 14] 
PALETTE_PINS = [1, 2, 3, 4, 5, 6]
LED_PINS = [8, 9, 10, 11, 12, 13]


# ==================== VARIABLES GLOBALES ====================
client_socket = None
connected = False
wlan = None
pot = None
buttons = {}
palette_sensors = []
leds = []
celebration_level = 0
celebration_step = 0
celebration_setp_timer = 0
celebration_duration = 3000
celebration_speed = 100
celebration_active = False
celebration_direction = 1

# ==================== CONTROL DE LEDs ====================
led_timers = [0] * 6
team_leds = {"local": False, "visit": False}
led_states = [0] * 6

def update_leds():
    """Actualizar todos los LEDs según estados actuales"""
    try:
        for i in range(min(6, len(leds))):
            if leds[i] is not None:
                leds[i].value(led_states[i])
    except Exception as e:

def check_led_timers():
    """Verificar y apagar LEDs después de 3 segundos"""
    current_time = time.ticks_ms()
    for i in range(6):
        if led_timers[i] != 0 and time.ticks_diff(current_time, led_timers[i]) > 3000:
            if not celebration_active or celebration_level < (i + 1):
                led_states[i] = 0
                led_timers[i] = 0
                
    update_celebration_animation()
    

# ==================== CLASES CORREGIDAS ====================
class Button:
    def __init__(self, pin_number, index):
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
        self.index = index
        self.name = f'btn{index}'
        self.last_state = True
        self.last_change_time = time.ticks_ms()
        self.debounce_delay = 80
        
    def read(self):
        current_state = self.pin.value() == 0
        current_time = time.ticks_ms()
        
        if current_state != self.last_state:
            if time.ticks_diff(current_time, self.last_change_time) > self.debounce_delay:
                self.last_state = current_state
                self.last_change_time = current_time

                
                return current_state, True
        
        return self.last_state, False

class PaletteSensor:
    def __init__(self, pin_number, index):
        self.index = index
        self.pin_number = pin_number
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_DOWN)
        self.active_state = 1
        self.mode_name = "3.3V con PULL-DOWN"
        
        self.activation_count = 0
        self.last_state = 0
        self.last_stable_state = 0
        self.last_change_time = time.ticks_ms()
        self.state_history = [0] * 5
        self.confidence_count = 0
        self.min_confidence = 5
        self.debounce_delay = 200
        self.min_activation_time = 300
        self.last_activation_time = 0
        
        # Mecanismo anti-congelamiento
        self.activation_lock = False
        self.lock_timeout = 500
        self.error_count = 0
        self.max_errors = 5

    def read(self):
        try:
            # Prevenir congelamiento por errores
            if self.error_count > self.max_errors:
                self.last_stable_state = 0
                self.activation_lock = False
                self.error_count = 0
                return 0, False
            
            # Verificar bloqueo temporal
            current_time = time.ticks_ms()
            if self.activation_lock:
                if time.ticks_diff(current_time, self.last_activation_time) > self.lock_timeout:
                    self.activation_lock = False
                else:
                    return self.last_stable_state, False
            
            raw_value = self.pin.value()
            
            # Filtro de mediana
            if len(self.state_history) > 0:
                self.state_history.pop(0)
            self.state_history.append(raw_value == self.active_state)
            
            true_count = sum(self.state_history)
            false_count = len(self.state_history) - true_count
            median_state = true_count > false_count
            
            # Lógica de detección
            if median_state != self.last_state:
                self.confidence_count = 0
                self.last_state = median_state
                self.last_change_time = current_time
            
            time_since_change = time.ticks_diff(current_time, self.last_change_time)
            if time_since_change > 20:
                self.confidence_count = min(self.confidence_count + 1, self.min_confidence * 2)
            
            state_changed = False
            if (self.confidence_count >= self.min_confidence and 
                median_state != self.last_stable_state and
                time_since_change > self.debounce_delay):
                
                if median_state:
                    time_since_last_activation = time.ticks_diff(current_time, self.last_activation_time)
                    if time_since_last_activation < self.min_activation_time:
                        return self.last_stable_state, False
                
                self.last_stable_state = median_state
                state_changed = True
                
                if median_state:
                    self.activation_count += 1
                    self.last_activation_time = current_time
                    # BLOQUEAR PARA EVITAR DOBLE DETECCIÓN
                    self.activation_lock = True
                               
            return self.last_stable_state, state_changed
            
        except Exception as e:
            self.error_count += 1
            return self.last_stable_state, False

# ==================== FUNCIONES PRINCIPALES ====================
def setup_hardware():
    global pot, buttons, palette_sensors, leds
    
    try:
        # Potenciómetro
        pot = ADC(POT_PIN)
        
        # Botones CORREGIDOS
        buttons = {}
        for i, pin in enumerate(BTN_PINS):
            btn = Button(pin, i + 1)
            buttons[btn.name] = btn
        
        # Sensores de paletas
        palette_sensors = []
        for i, pin in enumerate(PALETTE_PINS):
            sensor = PaletteSensor(pin, i)
            palette_sensors.append(sensor)
        
        # LEDs
        leds = []
        for i, pin in enumerate(LED_PINS):
            try:
                led = Pin(pin, Pin.OUT)
                leds.append(led)
            except Exception as e:
        
        return True
        
    except Exception as e:
        return False

def read_potentiometer():
    """Leer potenciómetro con filtrado anti-ruido"""
    try:
        if pot is None:
            return 0
            
        readings = []
        for i in range(3):
            readings.append(pot.read_u16() >> 6)
            time.sleep(0.001)
        return sum(readings) // len(readings)
    except Exception as e:
        return 0

def read_buttons():
    """Leer botones"""
    button_events = []
    try:
        for btn_name, btn in buttons.items():
            state, changed = btn.read()
            if changed and state:
                button_events.append((btn.index, state))
    except Exception as e:
    return button_events

def read_palettes():
    """Leer paletas"""
    palette_events = []
    try:
        for i, sensor in enumerate(palette_sensors):
            state, changed = sensor.read()
            if changed:
                palette_events.append((i, state))
                
        return palette_events
                
    except Exception as e:
        # Recuperación: reiniciar estados de paletas
        for sensor in palette_sensors:
            sensor.last_stable_state = 0
            sensor.activation_lock = False
            sensor.error_count = 0
    
    return palette_events

def connect_wifi():
    """Conectar a WiFi"""
    global wlan
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)        
        if wlan.isconnected():
            ip = wlan.ifconfig()[0]
            return True
        
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        for attempt in range(20):
            if wlan.isconnected():
                ip = wlan.ifconfig()[0]
                return True
            print(".", end='')
            time.sleep(0.5)
        
        return False
        
    except Exception as e:
        return False

def handle_command(command):
    """Manejar comandos del juego"""
    global team_leds, led_states, led_timers, celebration_level, celebration_active, celebration_timer
    
    if command.startswith("CMD:"):
        cmd = command[4:]
        
        try:
            # ==================== LEDs DE EQUIPO (H, I) ====================
            if cmd == "H":
                team_leds["local"] = True
            elif cmd == "I":
                team_leds["visit"] = True
            elif cmd == "H_OFF":
                team_leds["local"] = False
            elif cmd == "I_OFF":
                team_leds["visit"] = False
                
            # ==================== LEDs INDIVIDUALES POR 3s (J, K, L, M, N, O) ====================
            elif cmd in ["J", "K", "L", "M", "N", "O"]:
                led_index = ord(cmd) - ord('J')  # J=0, K=1, L=2, M=3, N=4, O=5
                if 0 <= led_index < 6:
                    led_states[led_index] = 1
                    led_timers[led_index] = time.ticks_ms()
                    
            # ==================== COMANDOS DE CELEBRACIÓN ====================
            elif cmd.startswith("CELEBRATE:"):
                # Formato: CELEBRATE:3
                level_str = cmd.split(":")[1]
                level = int(level_str)
                start_celebration(level)
                
            elif cmd == "CELEBRATE_MAX":
                start_celebration(6)  # MÁXIMA CELEBRACIÓN - GOL
                
            elif cmd == "CELEBRATE_MED":
                start_celebration(3)  # Celebración media
                
            elif cmd == "CELEBRATE_MIN": 
                start_celebration(1)  # Celebración mínima
                
            elif cmd == "CELEBRATE_STOP":
                celebration_active = False
                celebration_level = 0
                for i in range(6):
                    led_states[i] = 0
                update_leds()
                
            # ==================== COMANDOS ESPECIALES ====================
            elif cmd.startswith("TEAM_LED:"):
                team_type = cmd.split(":")[1]
                if team_type == "local":
                    team_leds["local"] = True
                    team_leds["visit"] = False
                elif team_type == "visit":
                    team_leds["local"] = False  
                    team_leds["visit"] = True
                    
            elif cmd == "LEDS_OFF":
                for i in range(6):
                    led_states[i] = 0
                    led_timers[i] = 0
                team_leds = {"local": False, "visit": False}
                celebration_active = False
                celebration_level = 0
                
            # ==================== ACTUALIZAR ESTADOS FÍSICOS ====================
            update_leds()  # Aplicar cambios físicos a los LEDs
                
        except Exception as e:
            print(f"Error procesando comando '{cmd}': {e}")

def send_message(sock, message):
    """Enviar mensaje al cliente"""
    try:
        sock.send((message + "\n").encode())
    except Exception as e:
        global connected
        connected = False

def handle_client(sock):
    """Manejar cliente conectado - CORREGIDO"""
    global connected
    last_pot_value = -1
    
    try:
        sock.setblocking(False)
        poll = uselect.poll()
        poll.register(sock, uselect.POLLIN)
        
        try:
            while connected:
                # Verificar timers de LEDs
                check_led_timers()
                
                # Leer sensores
                pot_value = read_potentiometer()
                if abs(pot_value - last_pot_value) > 5:
                    send_message(sock, f"POT:{pot_value}")
                    last_pot_value = pot_value
                
                button_events = read_buttons()
                for btn_num, state in button_events:
                    send_message(sock, f"BTN:{btn_num}:{1 if state else 0}")
                    time.sleep(0.02)
                
                palette_events = read_palettes()
                for palette_num, state in palette_events:
                    send_message(sock, f"PAL:{palette_num}:{1 if state else 0}")
                    time.sleep(0.02)
                
                events = poll.poll(10)
                if events:
                    try:
                        data = sock.recv(1024).decode().strip()
                        if data:
                            handle_command(data)
                    except:
                        break
                
                time.sleep(0.01)
                
        except Exception as e:
            print(f"Error en handle_client loop: {e}")
    except Exception as e:
        print(f"Error en handle_client setup: {e}")
    finally:
        connected = False
        try:
            sock.close()
        except:
            pass
        print("Cliente desconectado")

def start_server():
    """Iniciar servidor socket"""
    global client_socket, connected
    
    try:
        addr = socket.getaddrinfo('0.0.0.0', SERVER_PORT)[0][-1]
        server_socket = socket.socket()
        server_socket.bind(addr)
        server_socket.listen(1)
        
        print("SERVIDOR INICIADO - Puerto: {SERVER_PORT}")
        print("Esperando conexión...")
        
        poll = uselect.poll()
        poll.register(server_socket, uselect.POLLIN)
        
        while True:
            try:
                events = poll.poll(1000)
                if events:
                    client_socket, client_addr = server_socket.accept()
                    connected = True
                    _thread.start_new_thread(handle_client, (client_socket,))
                    
            except Exception as e:
                print(f"Error en servidor: {e}")
                time.sleep(1)
                
    except Exception as e:
        print(f"Error en start_server(): {e}")
        
def update_celebration_animation():
    """Actualizar animación progresiva mejorada"""
    global celebration_level, celebration_active, celebration_timer, celebration_step, celebration_step_timer, led_states, celebration_direction
    
    if not celebration_active:
        return
        
    current_time = time.ticks_ms()
    elapsed_total = time.ticks_diff(current_time, celebration_timer)
    
    # Verificar si terminó el tiempo de celebración
    if elapsed_total > celebration_duration:
        # Fin de la celebración - apagar todos los LEDs con efecto de apagado progresivo
        for i in range(6):
            led_states[i] = 0
        celebration_active = False
        celebration_level = 0
        celebration_step = 0
        update_leds()
        return
    
    # ANIMACIÓN PROGRESIVA
    elapsed_step = time.ticks_diff(current_time, celebration_step_timer)
    
    # Para niveles altos (4-6): efecto de ida y vuelta
    if celebration_level >= 4 and celebration_step >= celebration_level:
        if elapsed_step > celebration_speed:
            celebration_step_timer = current_time
            # Cambiar dirección
            celebration_direction *= -1
            if celebration_direction == 1:
                celebration_step = 0  # Reiniciar desde izquierda
            else:
                celebration_step = celebration_level - 1  # Empezar desde derecha
    
    # Para niveles bajos (1-3): efecto simple de progresión
    elif celebration_step < celebration_level and elapsed_step > celebration_speed:
        celebration_step += 1
        celebration_step_timer = current_time
    
    # ACTUALIZAR LEDs SEGÚN ANIMACIÓN
    for i in range(6):
        if celebration_direction == 1:  # Izquierda → Derecha
            led_states[i] = 1 if i < celebration_step else 0
        else:  # Derecha a izquierda
            led_states[i] = 1 if i >= (6 - celebration_step) else 0
    
    update_leds()

def start_celebration(level):
    """Iniciar animación progresiva de celebración según nivel (0-6)"""
    global celebration_level, celebration_active, celebration_timer, celebration_step, celebration_step_timer, celebration_direction
    celebration_level = min(max(level, 0), 6)  # Asegurar entre 0-6
    celebration_active = True
    celebration_timer = time.ticks_ms()
    celebration_step_timer = time.ticks_ms()
    celebration_step = 0
    celebration_direction = 1  # Siempre empezar de izquierda a derecha

def main():
    
    try:
        # Inicializar hardware
        if not setup_hardware():
            print("No se pudo inicializar el hardware. Verifica conexiones.")
            return
        
        # CONEXIÓN NORMAL
        if connect_wifi():
            start_server()
        else:
            error_count = 0
            while True:
                time.sleep(0.1)
                error_count += 1
                
    except Exception as e:
        print(f"Error crítico en main(): {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Programa interrumpido por el usuario")
    except Exception as e:
        print(f"ERROR CRÍTICO: {e}")
        print("Reiniciando en 5 segundos...")
        time.sleep(5)
        import machine
        machine.reset()