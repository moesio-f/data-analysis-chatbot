"""Instanciamento de agentes e memória."""

from chat.agents import data_analyst as da
from chat.entities import DataSource
from langgraph.checkpoint.memory import InMemorySaver

# Memória dos agentes (short-term)
_MEMORY: InMemorySaver = InMemorySaver()


def get_data_analyst_agent(ds: DataSource) -> da.CompiledStateGraph:
    """Retorna um agente analista de dados.

    Returns:
        CompiledStateGraph: agente analista
            de dados.
    """
    return da.create_agent(ds, memory=_MEMORY)
