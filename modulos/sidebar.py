import streamlit as st
from modulos.rotas import SIDEBAR_ITEMS
from modulos.utils.text_utils import formata_primeiro_nome

def renderizar_sidebar():
    """Renderiza a Sidebar completa"""
    renderizar_menu_navegacao()
    st.sidebar.divider()
    renderizar_perfil_usuario()

def renderizar_menu_navegacao():
    """Renderiza o menu principal de navegação"""
    st.sidebar.subheader("Menu principal")
    
    for item in SIDEBAR_ITEMS:
        if st.sidebar.button(
            f"{item['icon']} {item['label']}",
            key=f"nav_{item['id']}",
            use_container_width=True,
            type="primary" if st.session_state.pagina == item["id"] else "secondary",
        ):
            st.session_state.pagina = item["id"]
            st.rerun()

def renderizar_perfil_usuario():
    """Renderiza a seção de perfil do usuário"""

    nome_usuario = formata_primeiro_nome(st.user.name)
    st.sidebar.markdown(f"Olá, {nome_usuario}!")
    
    if st.sidebar.button(":material/logout: Logout", use_container_width=True):
        st.logout()
        st.stop()