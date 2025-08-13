"""Entrypoint do dashboard
com streamlit multi página.
"""

import streamlit as st

from app import patches

# Set page global configuration
st.set_page_config(page_title="Chatbot para Análise de Dados")

# Configure navigation bar
pg = st.navigation(
    [
        st.Page(
            "login/page.py", title="Login", icon=":material/home:", url_path="login"
        ),
        st.Page("chat/page.py", title="Chat", icon=":material/chat:", url_path="chat"),
    ],
    expanded=False,
)


# Apply patches
patches.apply_streamlit_patches()

# Run selected page
pg.run()
