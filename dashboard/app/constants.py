"""Constantes manipuladas pelo sistema."""

# Chave para dados do usuário (dict).
USER_DATA_KEY: str = "user_data"

# Chave para o histórico de mensagens (list[dict].
CHAT_HISTORY_KEY: str = "chat_history"


class UserInfoKeys:
    """Chaves relacionadas
    com dados do usuário.
    """

    data_source_id: str = "id"
    data_source_name: str = "name"
    data_source_description: str = "description"
    data_source_connector: str = "connector"
