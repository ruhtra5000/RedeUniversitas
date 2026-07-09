import streamlit as st

# Tentativa falha de interface

def telaHome():
    st.title("Rede Universitas")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):

            st.subheader("📁 Cadastros")

            st.write("Cadastre alunos, professores, cursos...")

            if st.button("Entrar"):
                st.session_state.pagina = "cadastro"
                st.rerun()

    with col2:
        with st.container(border=True):

            st.subheader("🎓 Acadêmico")

            if st.button("Entrar", key="acad"):
                st.session_state.pagina = "academico"
                st.rerun()