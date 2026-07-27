import streamlit as st

def telaHome():
    st.title("Rede Universitas")


    with st.container(horizontal=True):
        with st.container(border=True):
            st.subheader("📁 Cadastros")
            st.write("Cadastre alunos, professores, cursos...")

            if st.button("Entrar"):
                from modulos.rotas import cadastros_page # evita import circular
                st.switch_page(cadastros_page)

        with st.container(border=True):
            st.subheader("🎓 Acadêmico")
            
            # TODO: implementar e importar a academico_page quando for criada
            # if st.button("Entrar", key="acad"):
            #     from modulos.rotas import academico_page
            #     st.switch_page(academico_page)
