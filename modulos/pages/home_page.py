import streamlit as st

def telaHome():
    pessoa_nome = st.session_state.get("pessoa_logada", st.user.name)

    st.title("RedeUniversitas")
    st.write(f"Bem-vindo(a) de volta, **{pessoa_nome}**!")
    
    st.caption("Selecione uma aba pelo painel lateral para utilizar o sistema")