import os
import requests
from dotenv import load_dotenv

# Cargar credenciales desde el archivo .env
load_dotenv()

class TelegramNotifier:
    """Envía mensajes formateados a un chat de Telegram mediante su API oficial."""

    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_message(self, message: str) -> bool:
        """Despacha un texto usando formato Markdown."""
        if not self.token or not self.chat_id:
            print("❌ Error: Faltan credenciales de Telegram en el archivo .env")
            return False

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }

        try:
            response = requests.post(self.base_url, json=payload, timeout=10)
            if response.status_code == 200:
                return True
            print(f"⚠️ Error de Telegram API: {response.text}")
            return False
        except Exception as error:
            print(f"⚠️ Error al conectar con Telegram: {error}")
            return False