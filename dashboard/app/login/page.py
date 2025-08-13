"""Página para acesso ao chatbot."""

import streamlit as st
from app import client, constants, callbacks

user_data = st.session_state.get(constants.USER_DATA_KEY, dict())

# ====== Título ======
st.title("Login")
st.markdown(
    "Olá! Seja bem vindo ao sistema. Para interagir com o chatbot e demais functionalidades "
    "selecione uma fonte de dados abaixo ou registre uma nova."
)

# ====== Seleção ======
st.subheader("Selecionar Fonte de Dados", divider="gray")

if constants.UserInfoKeys.data_source_id in user_data:
    with st.container():
        st.info(
            "Você está atualmente conectado à "
            f"fonte de dados '{user_data[constants.UserInfoKeys.data_source_name]}'"
            f"({user_data[constants.UserInfoKeys.data_source_connector]})"
        )
        btn = st.button("Desconectar", on_click=callbacks.disconnect_user)
        if btn:
            st.rerun()

st.markdown("Para selecionar uma fonte de dados, escolha uma das opções abaixo.")
st.selectbox(
    "Qual fontes de dados você quer acessar hoje?",
    key=(key := "ds_selectbox"),
    options=client.DSClient.list_sources(),
    index=None,
    format_func=lambda d: f"{d['name']} ({d['connector']})",
    on_change=lambda: callbacks.update_user_data(key),
)

# ====== Cadastro ======
st.subheader("Cadastrar nova Fonte de Dados", divider="gray")
