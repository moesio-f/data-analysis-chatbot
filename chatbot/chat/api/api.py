"""Entrypoint da API
RESTFul para comunicação
com o chatbot.
"""

import textwrap
import logging
from typing import Annotated

from fastapi import Body, FastAPI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph.state import CompiledStateGraph

from .agent import get_data_analyst_agent
from .data_source import get_source

app = FastAPI()

LOGGER = logging.getLogger(__name__)


def run_agent(
    agent: CompiledStateGraph,
    messages: list[HumanMessage | SystemMessage],
    config: dict,
) -> str:
    """Executa o agente com a mensagem do usuário.

    Args:
        agent: agente a ser utilizado.
        message: mensagem do usuário.
        config: configurações da execução.

    Return:
        str: tokens produzidos pelo agente.
    """
    return agent.invoke({"messages": messages}, config)["messages"][-1].content


@app.post("/chat/{data_source_id}")
async def send_message_and_stream(
    data_source_id: int,
    message: Annotated[str, Body(media_type="text/plain; charset=utf-8")],
):
    """Realiza um turno de conversação com o agente de dados
    sobre a fonte de dados do request.

    A resposta é retornada em formato de _stream_ para melhor
    integração com UIs de chat.
    """
    LOGGER.debug(
        "Received message from user on data souce %d: '%s'",
        data_source_id,
        textwrap.shorten(message, width=80),
    )
    try:
        ds = get_source(data_source_id)
        agent = get_data_analyst_agent(ds)
    except Exception as e:
        LOGGER.error("Failed to create agent: %s", e, exc_info=True)
        raise

    LOGGER.debug("Data source and agent ready. Running agent...")
    try:
        answer = run_agent(
            agent,
            [
                SystemMessage(
                    "O usuário está acessando a seguinte fonte de dados:"
                    f"\n```json\n{ds.model_dump(mode="json", exclude="connector")}\n```"
                ),
                HumanMessage(message),
            ],
            {"configurable": {"thread_id": data_source_id}},
        )
        LOGGER.debug(
            "Agent answered with %d tokens: '%s'",
            len(answer),
            textwrap.shorten(answer, width=80),
        )
        return answer

    except Exception as e:
        LOGGER.error("Failed to run agent: %s", e, exc_info=True)
        raise


@app.get("/healthcheck")
async def healthcheck():
    """Healthcheck da API."""
    return "OK"
