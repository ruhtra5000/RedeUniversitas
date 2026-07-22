import streamlit as st
from modulos.rotas import ROTA_CADASTRO_ALUNO, ROTA_CADASTRO_PROFESSOR, ROTA_CADASTRO_CURSO, ROTA_CADASTRO_DISCIPLINA, ROTA_CADASTRO_TURMA

def telaCadastros():
    st.title("Cadastros")

    with st.container(horizontal=True):

        if st.button("Alunos"):
            st.session_state.pagina = ROTA_CADASTRO_ALUNO
            st.rerun()

        if st.button("Professores"):
            st.session_state.pagina = ROTA_CADASTRO_PROFESSOR
            st.rerun()

        if st.button("Cursos"):
            st.session_state.pagina = ROTA_CADASTRO_CURSO
            st.rerun()

        if st.button("Disciplinas"):
            st.session_state.pagina = ROTA_CADASTRO_DISCIPLINA
            st.rerun()

        if st.button("Turmas"):
            st.session_state.pagina = ROTA_CADASTRO_TURMA
            st.rerun()