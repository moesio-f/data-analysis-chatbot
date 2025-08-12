"""Interface para conectores."""

from abc import ABC, abstractmethod

import pandas as pd


class Connector(ABC):
    """Interface de um conector
    à uma fonte de dados.
    """

    def __init__(self, connection_string: str, table: str):
        self._url = connection_string
        self._table = table

    @property
    def connection_string(self) -> str:
        """String de conexão com a fonte
        de dados.

        Returns:
            str: string de conexão.
        """
        return self._url

    @property
    def table(self) -> str:
        """Nome da tabela padrão
        para realização das queries.

        Esse componente corresponde ao
        `name` de uma fonte de dados.

        Returns:
            str: nome da tabela.
        """
        return self._table

    @abstractmethod
    def connect(self):
        """Inicia uma conexão com a
        fonte de dados.

        Caso já conectado, ignora.
        """

    @abstractmethod
    def disconnect(self):
        """Encerra a conexão com a
        fonte de dados. Caso não tenha
        conexão, não realiza nenhuma
        operação.
        """

    @abstractmethod
    def query(self, query: str) -> pd.DataFrame:
        """Realiza uma query na fonte de
        dados.
        """
