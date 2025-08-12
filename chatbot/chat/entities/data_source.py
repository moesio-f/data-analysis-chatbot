"""Classes para metadados
de fontes de dados.
"""

from functools import cached_property

from pydantic import BaseModel, computed_field

from .connector import Connector


class Column(BaseModel):
    """Coluna de uma fonte de dados.

    Attributes:
        name: nome.
        description: descrição.
    """

    name: str
    description: str


class DataSource(BaseModel):
    """Fonte de dados.

    Attributes:
        connector: conector para
            a fonte de dados.
        name: nome.
        description: descrição.
        columns: colunas.
    """

    model_config = {"arbitrary_types_allowed": True}

    connector: Connector
    name: str
    description: str
    columns: list[Column]

    @computed_field
    @cached_property
    def column_dict(self) -> dict[str, Column]:
        return {c.name: c for c in self.columns}

    def has_column(self, column: str) -> bool:
        return self.column_dict.get(column) is not None
