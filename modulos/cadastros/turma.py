from sqlalchemy.exc import SQLAlchemyError
import streamlit as st

from database.Conexao import SessionLocal
from database.entidades.Turma import Turma
import database.entidades
from modulos.academico.academico_db import (dbListarCursos, dbListarDisciplinasGeral, dbListarProfessores)

# Interface
def telaCadastroTurma():

    if "form_key_turma" not in st.session_state:
        st.session_state.form_key_turma = 0

    st.title("🏫 Cadastro de Turma")
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
        st.toast("Turma cadastrada com sucesso!", icon="🎉")

    col1, col2 = st.columns([1, 6])

    with col1:
        if st.button("⬅ Voltar", use_container_width=True):
            st.session_state.pagina = "cadastros" 
            st.rerun()

    if "cache_cursos" not in st.session_state:
        st.session_state.cache_cursos = dbListarCursos()

    if "cache_disciplinas" not in st.session_state:
        st.session_state.cache_disciplinas = dbListarDisciplinasGeral()

    if "cache_professores" not in st.session_state:
        st.session_state.cache_professores = dbListarProfessores()

    lista_cursos = st.session_state.cache_cursos
    lista_disciplinas = st.session_state.cache_disciplinas
    lista_professores = st.session_state.cache_professores

    if not lista_cursos or not lista_disciplinas or not lista_professores:
        st.warning(
            """
            ⚠️ Antes de cadastrar uma turma é necessário possuir pelo menos:

            - **1 Curso**
            - **1 Disciplina**
            - **1 Professor**
            """
        )

    with st.form(key=f"cadastro_turma_{st.session_state.form_key_turma}", border=False):

        with st.container(border=True):
            st.subheader("📚 Dados da Turma")
            
            c1, c2 = st.columns(2)
            with c1:
                semestre = st.text_input(
                    "Semestre *",
                    placeholder="Ex.: 2026.1",
                    key=f"turma_semestre_{st.session_state.form_key_turma}"
                )
                
            with c2:
                curso_selecionado = st.selectbox(
                    "Curso *",
                    options=lista_cursos if lista_cursos else [],
                    format_func=lambda c: c.nome,
                    index=None,
                    placeholder="Selecione um curso...",
                    disabled=not lista_cursos,
                    key=f"turma_curso_{st.session_state.form_key_turma}"
                )

        st.write("")

        with st.container(border=True):
            st.subheader("🔗 Vínculos Acadêmicos")
            
            c3, c4 = st.columns(2)
            with c3:
                disciplina_selecionada = st.selectbox(
                    "Disciplina *",
                    options=lista_disciplinas if lista_disciplinas else [],
                    format_func=lambda d: d.nome,
                    index=None,
                    placeholder="Selecione uma disciplina...",
                    disabled=not lista_disciplinas,
                    help="A disciplina deve pertencer ao curso selecionado acima.",
                    key=f"turma_disciplina_{st.session_state.form_key_turma}"
                )
                
            with c4:
                professor_selecionado = st.selectbox(
                    "Professor *",
                    options=lista_professores if lista_professores else [],
                    format_func=lambda p: p.pessoa.nome,
                    index=None,
                    placeholder="Selecione um professor...",
                    disabled=not lista_professores,
                    help="O professor deve pertencer ao mesmo campus do curso.",
                    key=f"turma_professor_{st.session_state.form_key_turma}"
                )

        st.write("")

        _, centro, _ = st.columns([2, 3, 2])
        
        with centro:
            cadastrar = st.form_submit_button(
                "💾 Cadastrar Turma", 
                type="primary", 
                use_container_width=True
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
                    curso=curso_selecionado,
                    disciplina=disciplina_selecionada,
                    professor=professor_selecionado
                )
                
                criarTurma(turma=nova_turma)
                
                st.session_state.form_key_turma += 1 
                st.session_state["cadastro_turma_realizado"] = True
                
                st.rerun()
                
            except SQLAlchemyError as e:
                st.error(f"Erro no banco de dados: {e}")
            except Exception as e:
                st.error(str(e))

# Service
def criarTurma(turma: Turma):
    try:
        turma.codigo = ""
        
        if turma.curso_id != turma.disciplina.curso_id:
            raise Exception(f"A disciplina selecionada deve pertencer ao curso {turma.curso.nome}.")

        if turma.curso.campus_id != turma.professor.campus_id:
            raise Exception(f"O professor designado para esta Turma deve pertencer ao Campus {turma.curso.campus.nome}.")
        
        dbCriarTurma(turma)
            
    except SQLAlchemyError:    
        raise
    
    except Exception:
        raise


# Dados
def dbCriarTurma(turma: Turma):
    with SessionLocal() as session:
        try:
            session.add(turma)
            session.commit()
            session.refresh(turma)
            turma.codigo = f"{turma.disciplina.codigo}-{turma.id:05d}"
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise
