"""Configurações da API."""

from operator import call

from pydantic_settings import BaseSettings


@call
class settings(BaseSettings):
    """Configurações da API.

    Attributes:
        database_url: string de conexão
            com o banco de dados.
    """

    database_url: str = "sqlite:///data_sources.sqlite"
    run_with_debug: bool = False
