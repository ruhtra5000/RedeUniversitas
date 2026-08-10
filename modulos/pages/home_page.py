import streamlit as st

from modulos.utils.home_visual import renderizarHome

def telaHome():
    pessoa_nome = st.session_state.get(
        "pessoa_logada",
        st.user.name,
    )

    renderizarHome(pessoa_nome) 