"""Cliente para consumo
da API do chatbot.
"""

from operator import call

import requests
from app.config import settings


@call
class ChatClient:
    def __init__(self):
        self._url = settings.chatbot_url

    def chat(self, ds_id: int, message: str) -> str:
        """Envia uma mensagem para o chatbot
        e retorna a resposta.

        Args:
            ds_id: id da fonte de dados.
            message: mensagem do usuário.

        Returns:
            str: resposta do chatbot.
        """
        response = requests.post(
            f"{self._url.rstrip('/')}/chat/{ds_id}",
            data=message,
            headers={"Content-Type": "text/plain; charset=utf-8"},
        )
        response.raise_for_status()
        return response.json()
