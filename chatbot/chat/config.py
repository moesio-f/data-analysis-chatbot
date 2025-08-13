"""Configurações do chatbot."""

from operator import call

from pydantic_settings import BaseSettings


@call
class model_settings(BaseSettings):
    """Configurações dos modelos
    utilizados pelos agentes.

    Attributes:
        model: nome do modelo.
        provider: provedor do modelo.
    """

    model: str = "gpt-oss:20b"
    provider: str = "ollama"


@call
class data_source_api_settings(BaseSettings):
    """Configurações da API das fontes
    de dados.
    """

    model_config = {"env_prefix": "DATA_SOURCE_"}
    url: str
