"""Callbacks."""

import streamlit as st
from app import constants


def update_user_data(key: str):
    """Atualiza o estado de usuário através
    das informações de um data_source.

    Args:
        data_source: fonte de dados para o
            usuário.
    """
    disconnect_user()
    data_source = st.session_state.get(key)
    if not data_source:
        return

    if constants.USER_DATA_KEY not in st.session_state:
        st.session_state[constants.USER_DATA_KEY] = dict()

    for target_key, data_key in zip(
        [
            constants.UserInfoKeys.data_source_id,
            constants.UserInfoKeys.data_source_name,
            constants.UserInfoKeys.data_source_description,
            constants.UserInfoKeys.data_source_connector,
        ],
        ["id", "name", "description", "connector"],
    ):
        st.session_state[constants.USER_DATA_KEY][target_key] = data_source[data_key]


def disconnect_user():
    """Desconecta um usuário."""
    st.session_state[constants.USER_DATA_KEY] = dict()
    st.session_state[constants.CHAT_HISTORY_KEY] = []
