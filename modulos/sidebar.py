import streamlit as st
from modulos.utils.text_utils import formata_primeiro_nome

def renderizar_perfil_usuario():
    """Renderiza a seção de perfil do usuário"""

    nome_usuario = formata_primeiro_nome(st.user.name)
    st.markdown(f"**Olá, {nome_usuario}!**")
    
    if st.button(":material/logout: Logout", use_container_width=True):
        st.logout()
        st.stop()