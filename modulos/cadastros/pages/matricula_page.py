from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from database.Conexao import SessionLocal
from database.entidades.Matricula import Matricula
from modulos.cadastros.matricula import criarMatricula
from modulos.academico.academico_service import listarAlunos, listarTurmasGeral
import database.entidades

def telaCadastroMatricula():
    if "form_key_matr" not in st.session_state:
        st.session_state.form_key_matr = 0

    st.title("🎓 Cadastro de Matrícula")
    st.caption("Preencha as informações abaixo para matricular um aluno em uma turma.")

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

    if st.session_state.pop("cadastro_matr_realizado", False):
        st.toast("Matrícula realizada com sucesso!", icon=":material/check:")

    col1, _ = st.columns([1, 6])
    with col1:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import cadastros_page
            st.switch_page(cadastros_page)

    if "cache_alunos" not in st.session_state:
        st.session_state.cache_alunos = listarAlunos()

    if "cache_turmas" not in st.session_state:
        st.session_state.cache_turmas = listarTurmasGeral()

    lista_alunos = st.session_state.cache_alunos
    lista_turmas = st.session_state.cache_turmas

    if not lista_alunos or not lista_turmas:
        st.warning(
            """
            ⚠️ Antes de matricular um aluno é necessário possuir:
            - Pelo menos **1 Aluno**
            - Pelo menos **1 Turma**
            """
        )

    with st.container(border=False):
        
        with st.container(border=True):
            st.subheader("📚 Informações da Matrícula")
            
            with st.container(horizontal=True):
                aluno_selecionado = st.selectbox(
                    "Aluno *",
                    options=lista_alunos if lista_alunos else [],
                    format_func=lambda a: f"{a.pessoa.nome} - {a.matricula}",
                    index=None,
                    placeholder="Selecione um aluno...",
                    disabled=not lista_alunos,
                    key=f"matr_aluno_{st.session_state.form_key_matr}"
                )
                
                if aluno_selecionado:
                    turmas_filtradas = [t for t in lista_turmas if t.curso_id == aluno_selecionado.curso_id]
                else:
                    turmas_filtradas = []

                turma_selecionada = st.selectbox(
                    "Turma *",
                    options=turmas_filtradas,
                    format_func=lambda t: f"{t.codigo} - {t.disciplina.nome}",
                    index=None,
                    placeholder="Selecione uma turma..." if aluno_selecionado else "Selecione o Aluno primeiro",
                    disabled=not aluno_selecionado,
                    help="A disciplina da turma deve pertencer ao mesmo curso do aluno.",
                    key=f"matr_turma_{st.session_state.form_key_matr}"
                )

        st.write("")

        _, centro, _ = st.columns([2, 3, 2])
        with centro:
            cadastrar = st.button(
                "💾 Matricular Aluno", 
                type="primary", 
                use_container_width=True,
                key=f"btn_cad_matr_{st.session_state.form_key_matr}"
            )

    if cadastrar:
        if not lista_alunos or not lista_turmas:
            st.error("Cadastre os requisitos básicos antes de continuar.")
        elif aluno_selecionado is None:
            st.error("Por favor, selecione um Aluno.")
        elif turma_selecionada is None:
            st.error("Por favor, selecione uma Turma.")
        else:
            try:
                nova_matricula = Matricula(
                    aluno_id=aluno_selecionado.pessoa_id,
                    turma_id=turma_selecionada.id,
                    disciplina_id=turma_selecionada.disciplina_id,
                    aprovacao=None
                )
                
                criarMatricula(
                    matricula=nova_matricula,
                    aluno=aluno_selecionado,
                    disciplina=turma_selecionada.disciplina
                )
                
                st.session_state.form_key_matr += 1
                st.session_state["cadastro_matr_realizado"] = True
                st.session_state.pop("cache_turmas", None)
                st.rerun()
                
            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(str(e))