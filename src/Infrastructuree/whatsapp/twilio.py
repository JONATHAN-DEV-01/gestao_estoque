# src/Infrastructuree/whatsapp/twilio.py
import os
from twilio.rest import Client

class TwilioService:
    def __init__(self):
        # Usamos os nomes das variáveis do seu .env
        self.sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
        self.client = None
        
        if self.sid and self.token:
            self.client = Client(self.sid, self.token)

    def send_whatsapp_code(self, to_number: str, code: str) -> bool:
        """Envia o código de ativação via WhatsApp."""
        if not self.client or not self.from_number:
            print("[AVISO] Twilio não configurado. Pulando envio do WhatsApp.")
            return False

        try:
            # Garante que os números estão no formato correto
            self.client.messages.create(
                body=f"Seu código de ativação é: {code}",
                from_=f"{self.from_number}",
                to=f"{to_number}",
            )
            return True
        except Exception as e:
            print(f"Erro ao enviar WhatsApp para {to_number}:", e)
            return False