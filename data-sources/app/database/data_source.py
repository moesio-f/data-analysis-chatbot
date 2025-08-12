"""Definição de um Data Source
para o banco da aplicação.
"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger, Integer

from .connector import Connector


class Base(DeclarativeBase):
    pass


class ColumnDescription(Base):
    """Tabela que possui descrições
    das diferentes colunas de uma
    fonte de dados.

    Attributes:
        data_source_id: identificador da
            fonte de dados.
        column: nome da coluna.
        description: descrição da coluna.
        data_source: referência para o objeto
            da fonte dados.
    """

    __tablename__ = "column_description"

    data_source_id = mapped_column(
        ForeignKey("data_source.id", ondelete="CASCADE"), primary_key=True
    )
    name: Mapped[str] = mapped_column(
        primary_key=True, index=True, comment="Nome da coluna (as-is)."
    )
    description: Mapped[str] = mapped_column(
        nullable=False, comment="Descrição do que essa coluna representa."
    )
    data_source: Mapped["DataSource"] = relationship(
        back_populates="columns", cascade="all, delete"
    )


class DataSource(Base):
    """Representação de uma fonte
    de dados. No contexto do sistema,
    a definição é similar de um dataset.

    Uma fonte de dados é um objeto estruturado
    que representa uma coleção de entidades.

    Toda fonte de dados é composta por
    uma ou mais colunas, que descrevem
    um atributo da entidade representada
    em uma dada linha.

    Attributes:
        id: identificador único da fonte de
            dados.
        name: nome da fonte de dados.
        description: descrição da fonte
            de dados.
        columns: colunas presentes nessa
            fonte de dados.
    """

    __tablename__ = "data_source"

    id = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        comment="ID automático de provento.",
    )
    name: Mapped[str] = mapped_column(
        unique=True, index=True, comment="Nome da fonte de dados."
    )
    description: Mapped[str] = mapped_column(
        nullable=False, comment="Descrição da fonte de dados."
    )
    connection_string: Mapped[str] = mapped_column(
        nullable=False, comment="URL para conexão com a fonte de dados."
    )
    connector: Mapped[Connector] = mapped_column(
        nullable=False,
        index=True,
        comment="Conector que deve ser utilizado com a URL de conexão.",
    )
    columns: Mapped[list[ColumnDescription]] = relationship(
        back_populates="data_source"
    )
