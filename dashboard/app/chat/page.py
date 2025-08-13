"""Página de conversação com
o chatbot.
"""

import streamlit as st
from app import client, constants

ds_id = st.session_state.get(constants.USER_DATA_KEY, dict()).get(
    constants.UserInfoKeys.data_source_id
)

if not ds_id:
    st.error("Realize o login antes de conversar com o chat!")
else:
    if constants.CHAT_HISTORY_KEY not in st.session_state:
        st.session_state[constants.CHAT_HISTORY_KEY] = []

    # Adiciona o histórico da conversa
    for message in st.session_state[constants.CHAT_HISTORY_KEY]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Obtendo mensagem do usuário
    if prompt := st.chat_input("Escreva aqui..."):
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state[constants.CHAT_HISTORY_KEY].append(
            {"role": "user", "content": prompt}
        )

        # Obtendo resposta
        response = client.ChatClient.chat(ds_id, prompt)
        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state[constants.CHAT_HISTORY_KEY].append(
            {"role": "assistant", "content": response}
        )
