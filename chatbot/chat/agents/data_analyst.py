"""Agente analista de dados.

A definição desse agente se baseia na
noção de "agent profile" definida no
seguinte artigo:

Li, X., Wang, S., Zeng, S. et al.
A survey on LLM-based multi-agent systems: workflow,
infrastructure, and challenges. Vicinagearth 1, 9 (2024).
"""

from copy import deepcopy

import yaml
from chat.config import model_settings as settings
from chat.entities import DataSource
from chat.tools.query import run_sql_select
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import chain
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langgraph.types import Checkpointer

# Prompt do perfil do agente
with open("chat/agents/prompts/profiles.yaml") as f:
    _PROMPT = yaml.full_load(f)["data_analyst"]

# Tools utilizadas pelo chat
_TOOLS = [run_sql_select]

# Modelo compartilhado para agentes analista
#   de dados.
_MODEL = init_chat_model(
    model=settings.model, model_provider=settings.provider
).bind_tools(_TOOLS)


def chatbot(state: MessagesState) -> MessagesState:
    """Nó do chatbot.

    Args:
        state: estado atual.

    Returns:
        MessagesState: novo estado.
    """
    # The agent might not have a prompt
    messages = state["messages"]
    if isinstance(messages[0], HumanMessage):
        messages = [SystemMessage(_PROMPT)] + messages

    return {"messages": [_MODEL.invoke(messages)]}


def inject_ds(agent: CompiledStateGraph, ds: DataSource) -> CompiledStateGraph:
    """Realiza a injeção da fonte de
    dados.

    Args:
        agent: agente.
        ds: fonte de dados.

    Returns:
        CompiledStateGraph: agente capaz de
            realizar queries nessa fonte
            de dados.
    """

    @chain
    def inject_param(state: MessagesState) -> MessagesState:
        ai_msg = state["messages"][-1]
        tool_calls = []
        for tool_call in ai_msg.tool_calls:
            tool_call_copy = deepcopy(tool_call)
            tool_call_copy["args"]["ds"] = ds
            tool_calls.append(tool_call_copy)
        ai_msg.tool_calls = tool_calls
        return state

    return agent | inject_param


def create_agent(memory: Checkpointer = None, **kwargs) -> CompiledStateGraph:
    """Cria o grafo de um agente analista de dados.

    Esse agente possui ferramentas para comunicação
    com fontes de dados.

    Args:
        memory: componente opcional de memória.

    Returns:
        CompiledStateGraph: grafo do Langchain
            representando o agente.
    """
    # State
    builder = StateGraph(MessagesState)

    # Nodes
    builder.add_node("chatbot", chatbot)
    builder.add_node("tools", ToolNode(_TOOLS))

    # Start flow
    builder.add_edge(START, "chatbot")

    # Tool calling or end
    builder.add_conditional_edges(
        "chatbot", tools_condition, {"tools": "tools", END: END}
    )

    # Tool has finished, return to chatbot
    builder.add_edge("tools", "chatbot")

    # Build graph
    return builder.compile(checkpointer=memory)
