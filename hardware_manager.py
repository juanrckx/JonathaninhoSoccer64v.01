import socket
import threading
import json


class HardwareManager:
    def __init__(self):
        self.server_ip = "192.168.18.237"  # IP
        self.server_port = 1717 
        self.client_socket = None
        self.connected = False
        self.potentiometer_value = 0
        self.button_states = {"btn1": False, "btn2": False, "btn3": False}
        self.palette_states = [False] * 6
        self.callbacks = {}

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # CORREGIDO: usar server_port
            self.client_socket.connect((self.server_ip, self.server_port))
            self.client_socket.settimeout(0.1)  # Timeout para no bloquear
            self.connected = True

            # Iniciar hilo para recibir mensajes
            threading.Thread(target=self._receive_messages, daemon=True).start()
            print(f"✅ Conectado al hardware en {self.server_ip}:{self.server_port}")
            return True
        except Exception as e:
            print(f"❌ Error conectando al hardware: {e}")
            return False

    def _receive_messages(self):
        buffer = ""
        while self.connected:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    print("Conexión cerrada por el servidor")
                    break

                buffer += data
                lines = buffer.split('\n')

                # Procesar líneas completas
                for line in lines[:-1]:
                    line = line.strip()
                    if line:
                        self._parse_hardware_message(line)

                buffer = lines[-1]  # Guardar línea incompleta

            except socket.timeout:
                continue  # Timeout normal, continuar
            except Exception as e:
                print(f"Error recibiendo datos: {e}")
                break

    def _parse_hardware_message(self, message):
        print(f"RAW: {message}")
        """Interpreta mensajes del hardware según el protocolo"""
        try:
            print(f"📨 Mensaje recibido: {message}")  # DEBUG

            if message.startswith("POT:"):
                value = int(message.split(":")[1])
                self.potentiometer_value = value
                self._trigger_callback("potentiometer", value)

            elif message.startswith("BTN:"):
                parts = message.split(":")
                btn_num = int(parts[1])
                state = parts[2] == "1"

                btn_name = f"btn{btn_num}"
                self.button_states[btn_name] = state
                self._trigger_callback("button", {"button": btn_name, "state": state})

            elif message.startswith("PAL:"):
                parts = message.split(":")
                pal_num = int(parts[1])
                state = parts[2] == "1"

                if 0 <= pal_num < 6:
                    self.palette_states[pal_num] = state
                    self._trigger_callback("palette", {"palette": pal_num, "state": state})

        except Exception as e:
            print(f"Error parseando mensaje '{message}': {e}")

    def register_callback(self, event_type, callback):
        """Registra callbacks para eventos del hardware"""
        if event_type not in self.callbacks:
            self.callbacks[event_type] = []
        self.callbacks[event_type].append(callback)
        print(f"📝 Callback registrado para: {event_type}")

    def _trigger_callback(self, event_type, data):
        """Ejecuta callbacks registrados"""
        if event_type in self.callbacks:
            for callback in self.callbacks[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error en callback {event_type}: {e}")

    def send_command(self, command):
        """Envía comandos al hardware (para feedback, LEDs, etc.)"""
        if self.connected:
            try:
                full_command = f"CMD:{command}\n"
                self.client_socket.send(full_command.encode())
                print(f"📤 Comando enviado: {command}")
            except Exception as e:
                print(f"Error enviando comando: {e}")

    def disconnect(self):
        self.connected = False
        if self.client_socket:
            self.client_socket.close()
        print("🔌 Hardware desconectado")