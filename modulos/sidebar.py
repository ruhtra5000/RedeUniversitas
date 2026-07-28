import streamlit as st
from modulos.utils.text_utils import formata_primeiro_nome

def renderizar_perfil_usuario():
    """Renderiza a seção de perfil do usuário"""

    nome_usuario = formata_primeiro_nome(st.session_state.get("pessoa_logada", st.user.name))
    
    st.markdown(f"**Olá, {nome_usuario}!**")
    
    # Exibir cargos formatados
    roles = st.session_state.get("roles", [])
    if roles:
        roles_formatadas = " • ".join([r.title() for r in roles])
        st.caption(f"*{roles_formatadas}*")

        # st.badge("Home", color="blue")

    
    if st.button(":material/logout: Logout", use_container_width=True):
        st.logout()
        st.stop()