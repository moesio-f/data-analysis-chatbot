"""Ferramenta básica
para consultas em fontes
de dados utilizando sintaxe
ANSI SQL.
"""

import logging
from typing import Callable, Optional

from chat.entities import DataSource
from langchain_core.tools import tool

from .exceptions import InvalidTable

LOGGER = logging.getLogger(__name__)


def generate_query_tool(ds: DataSource) -> Callable:
    """Gera uma ferramenta para
    realizar queries na fonte de
    dados.

    Args:
        ds: fonte de dados.

    Returns:
        Callable: tool do langchain.
    """

    @tool(
        parse_docstring=True,
        description="Permite realizar buscas na fonte/banco "
        "de dados do usuário. Deve ser utilizado para responder "
        "perguntas sobre os dados.",
    )
    def run_sql_select(
        table: str,
        select_columns: list[str],
        where_clause: Optional[str] = "",
        group_by: Optional[str] = "",
        having: Optional[str] = "",
        order_by: Optional[str] = "",
        limit: Optional[int] = -1,
    ) -> list[dict]:
        """Realize uma consulta SELECT usando
        SQL. Permite o uso de operações (e.g., SUM)
        ordenamento, filtros, e agrupamento.

        Args:
            table (str): tabela a ser utilizada na
                consulta.
            select_columns (list[str]): colunas utilizadas
                na consulta.
            where_clause (str): filtragem WHERE.
            group_by (str): cláusula de agrupamento GROUP BY.
            having (str): cláusula de agrupamento HAVING.
            order_by (str): cláusula de ordenação ORDER BY.

        Returns:
            list[dict]: resultado da consulta,
                cada elemento da lista corresponde
                à uma linha.
        """
        LOGGER.debug("Agent called tool with options: %s", locals())
        if table != ds.name:
            # In the future we might allow data sources
            #   with multiple tables.
            raise InvalidTable("Invalid table for data source '%s'.", ds.name)

        # Dynamic query construction
        # WARNING:. currently unsafe, allows for SQL injection;
        #   Should use prepared statements and other strategies
        #   for dynamic generation when creating PRC.
        sql = [f"SELECT {','.join(select_columns)} FROM '{table.strip("'")}'"]

        if where_clause:
            sql.append(f" WHERE {where_clause}")

        if group_by:
            sql.append(f" GROUP BY {group_by}")

        if having:
            sql.append(f" HAVING {having}")

        if order_by:
            sql.append(f" ORDER BY {order_by}")

        if limit > 0:
            sql.append(f" LIMIT {limit}")

        LOGGER.debug("Running query: %s", sql)
        try:
            res = ds.connector.query("".join(sql)).to_dict(orient="records")
        except Exception as e:
            LOGGER.error("Failed to run query: %s", e, exc_info=True)
            raise
        LOGGER.debug("Query returned: %s", res)
        return res

    return run_sql_select
