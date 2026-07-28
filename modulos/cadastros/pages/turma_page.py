from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from database.Conexao import SessionLocal
from database.entidades.Turma import Turma
import database.entidades
from modulos.academico.academico_service import (listarCursos, listarDisciplinasGeral, listarProfessores)
from modulos.cadastros.turma import criarTurma

def telaCadastroTurma():

    if "form_key_turma" not in st.session_state:
        st.session_state.form_key_turma = 0

    col1, _ = st.columns([1, 6])

    with col1:
        if st.button(":material/arrow_back: Voltar", width="stretch"):
            from modulos.rotas import cadastros_page # evita import circular
            st.switch_page(cadastros_page)

    st.title(":material/group_add: Cadastro de Turma")
    st.caption("Preencha as informações abaixo para cadastrar uma nova turma.")

    st.markdown(
        """
        <style>
        div[data-testid="InputInstructions"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.pop("cadastro_turma_realizado", False):
        st.toast("Turma cadastrada com sucesso!", icon=":material/check:")

    if "cache_cursos" not in st.session_state:
        st.session_state.cache_cursos = listarCursos()

    if "cache_professores" not in st.session_state:
        st.session_state.cache_professores = listarProfessores()
        
    if "cache_disciplinas" not in st.session_state:
        st.session_state.cache_disciplinas = listarDisciplinasGeral()

    lista_cursos = st.session_state.cache_cursos
    lista_disciplinas = st.session_state.cache_disciplinas
    lista_professores = st.session_state.cache_professores

    if not lista_cursos or not lista_disciplinas or not lista_professores:
        st.warning(
            """
            :material/warning: Antes de cadastrar uma turma é necessário possuir pelo menos:

            - **1 Curso**
            - **1 Disciplina**
            - **1 Professor**
            """
        )

    with st.container(border=False):

        with st.container():
            st.subheader("Dados da Turma")
            
            with st.container(horizontal=True):
                curso_selecionado = st.selectbox(
                    "Curso *",
                    options=lista_cursos if lista_cursos else [],
                    format_func=lambda c: c.nome,
                    index=None,
                    placeholder="Selecione um curso...",
                    disabled=not lista_cursos,
                    key=f"turma_curso_{st.session_state.form_key_turma}"
                )
                
                if curso_selecionado:
                    disciplinas_filtradas = [d for d in lista_disciplinas if d.curso_id == curso_selecionado.id]
                else:
                    disciplinas_filtradas = []

                disciplina_selecionada = st.selectbox(
                    "Disciplina *",
                    options=disciplinas_filtradas,
                    format_func=lambda d: d.nome,
                    index=None,
                    placeholder="Selecione uma disciplina..." if curso_selecionado else "Selecione o Curso primeiro",
                    disabled=not curso_selecionado,
                    key=f"turma_disc_{st.session_state.form_key_turma}"
                )

            with st.container(horizontal=True):
                professor_selecionado = st.selectbox(
                    "Professor *",
                    options=lista_professores if lista_professores else [],
                    format_func=lambda p: p.pessoa.nome,
                    index=None,
                    placeholder="Selecione um professor...",
                    disabled=not lista_professores,
                    key=f"turma_prof_{st.session_state.form_key_turma}"
                )
                semestre = st.text_input(
                    "Semestre *",
                    placeholder="Ex.: 2026.1",
                    key=f"turma_semestre_{st.session_state.form_key_turma}"
                )

        st.write("")

        _, centro, _ = st.columns([2, 3, 2])
        
        with centro:
            cadastrar = st.button(
                "Cadastrar Turma", 
                type="primary", 
                width="stretch",
                key=f"btn_cad_turma_{st.session_state.form_key_turma}"
            )

    # Processamento
    if cadastrar:
        if not lista_cursos or not lista_disciplinas or not lista_professores:
            st.error("Cadastre os requisitos básicos (Curso, Disciplina e Professor) antes de continuar.")
        elif not semestre.strip():
            st.error("Por favor, preencha o Semestre.")
        elif curso_selecionado is None:
            st.error("Por favor, selecione um Curso.")
        elif disciplina_selecionada is None:
            st.error("Por favor, selecione uma Disciplina.")
        elif professor_selecionado is None:
            st.error("Por favor, selecione um Professor.")
        else:
            try:
                nova_turma = Turma(
                    semestre=semestre.strip(),
                    codigo="",
                    curso_id=curso_selecionado.id,
                    disciplina_id=disciplina_selecionada.id,
                    professor_id=professor_selecionado.pessoa_id
                )
                
                criarTurma(
                    turma=nova_turma,
                    curso=curso_selecionado,
                    disciplina=disciplina_selecionada,
                    professor=professor_selecionado
                )
                
                st.session_state.form_key_turma += 1 
                st.session_state["cadastro_turma_realizado"] = True
                st.session_state.pop("cache_turmas", None)
                st.rerun()
                
            except SQLAlchemyError as e:
                st.error(f"Erro no banco de dados: {e}")
            except Exception as e:
                st.error(str(e))