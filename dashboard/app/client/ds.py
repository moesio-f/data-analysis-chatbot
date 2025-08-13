"""Client para consumo
da API de fontes de dados.
"""

from operator import call

import requests
from app.config import settings


@call
class DSClient:
    def __init__(self):
        self._url = settings.data_source_url

    def list_sources(self) -> list[dict]:
        """Obtém a lista de todas as
        fontes de dados cadastradas.

        Returns:
            list[dict]: todas fontes de
                dados disponíveis.
        """
        response = requests.get(f"{self._url.rstrip('/')}/list")
        response.raise_for_status()
        return response.json()
