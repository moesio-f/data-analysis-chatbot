"""Agente analista de dados.

A definição desse agente se baseia na
noção de "agent profile" definida no
seguinte artigo:

Li, X., Wang, S., Zeng, S. et al.
A survey on LLM-based multi-agent systems: workflow,
infrastructure, and challenges. Vicinagearth 1, 9 (2024).
"""

import yaml
from chat.config import model_settings as settings
from chat.entities import DataSource
from chat.tools.query import generate_query_tool
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langgraph.types import Checkpointer

# Prompt do perfil do agente
with open("chat/agents/prompts/profiles.yaml") as f:
    _PROMPT = yaml.full_load(f)["data_analyst"]


# Modelo base compartilhado entre agentes analistas.
_MODEL = init_chat_model(model=settings.model, model_provider=settings.provider)


def create_agent(
    ds: DataSource, memory: Checkpointer = None, **kwargs
) -> CompiledStateGraph:
    """Cria o grafo de um agente analista de dados.

    Esse agente possui ferramentas para comunicação
    com fontes de dados.

    Args:
        memory: componente opcional de memória.

    Returns:
        CompiledStateGraph: grafo do Langchain
            representando o agente.
    """
    # Inicialização
    tools = [generate_query_tool(ds)]
    model = _MODEL.bind_tools(tools)

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

        return {"messages": [model.invoke(messages)]}

    # State
    builder = StateGraph(MessagesState)

    # Nodes
    builder.add_node("chatbot", chatbot)
    builder.add_node("tools", ToolNode(tools))

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
