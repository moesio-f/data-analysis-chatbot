"""Modelos manipulados pela
API.
"""

from app.database import Connector
from pydantic import BaseModel


class Column(BaseModel):
    """Coluna de uma fonte de
    dados.

    Attributes:
        name: nome da coluna.
        description: descrição da coluna.
    """

    model_config = {"from_attributes": True}

    name: str
    description: str


class DataSourceInput(BaseModel):
    """Fonte de dados sem ID. Esse modelo
    deve ser utilizado como entrada para
    criação de novas fontes de dados.

    Attributes:
        name: nome do conjunto de dados.
        description: descrição do conjunto de dados.
        columns: colunas presentes nessa fonte
            de dados.
    """

    model_config = {"from_attributes": True}

    name: str
    description: str
    columns: list[Column]
    connection_string: str
    connector: Connector


class DataSource(DataSourceInput):
    """Fonte de dados.

    Attributes:
        id: identificador.
        name: nome do conjunto de dados.
        description: descrição do conjunto de dados.
        columns: colunas presentes nessa fonte
            de dados.
    """

    model_config = {"from_attributes": True}

    id: int
