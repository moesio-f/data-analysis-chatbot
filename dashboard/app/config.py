"""Configurações do dashboard."""

from operator import call

from pydantic_settings import BaseSettings


@call
class settings(BaseSettings):
    """Configurações globais.

    Attributes:
        data_source_url: URL para a API
            de fonte de dados.
        chatbot_url: URL para a API do
            chatbot.
    """

    data_source_url: str
    chatbot_url: str
