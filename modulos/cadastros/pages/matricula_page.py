import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from database.entidades.Matricula import Matricula
from modulos.academico.academico_service import (listarAlunos, listarTurmasGeral)
from modulos.cadastros.matricula import criarMatricula
from modulos.utils.cadastro_visual import (painelCadastro, renderizarAvisoCadastro, renderizarBotaoCadastro, renderizarSecaoCadastro, renderizarTopoCadastro)

# Tela de cadastro para Matrículas
def telaCadastroMatricula():
    if "form_key_matr" not in st.session_state:
        st.session_state.form_key_matr = 0

    # Função para voltar à página de cadastros
    def voltarCadastros():
        from modulos.rotas import cadastros_page

        st.switch_page(cadastros_page)

    renderizarTopoCadastro(
        titulo="Cadastrar matrícula",
        descricao=(
            "Vincule um aluno a uma turma compatível com seu " "curso acadêmico."
        ),
        aoVoltar=voltarCadastros,
        prefixoChave="cadastro_matricula",
    )

    if st.session_state.pop("cadastro_matr_realizado", False):
        st.toast(
            "Matrícula realizada com sucesso!",
            icon=":material/check:",
        )

    if "cache_alunos" not in st.session_state:
        st.session_state.cache_alunos = listarAlunos()

    if "cache_turmas" not in st.session_state:
        st.session_state.cache_turmas = listarTurmasGeral()

    lista_alunos = st.session_state.cache_alunos
    lista_turmas = st.session_state.cache_turmas

    if not lista_alunos or not lista_turmas:
        renderizarAvisoCadastro(
            titulo="Aluno e turma necessários",
            descricao=(
                "Cadastre pelo menos um aluno e uma turma antes "
                "de realizar a matrícula."
            ),
        )

    with painelCadastro(
        titulo="Informações da matrícula",
        descricao=(
            "Selecione o aluno para visualizar somente as "
            "turmas compatíveis com seu curso."
        ),
    ):

        renderizarSecaoCadastro(
            numero=1,
            titulo="Vínculo acadêmico",
            descricao="Aluno e turma que formarão a matrícula.",
        )

        colAluno, colTurma = st.columns(2)

        with colAluno:
            aluno_selecionado = st.selectbox(
                "Aluno *",
                options=lista_alunos if lista_alunos else [],
                format_func=(
                    lambda aluno: (f"{aluno.pessoa.nome} - {aluno.matricula}")
                ),
                index=None,
                placeholder="Selecione um aluno...",
                disabled=not lista_alunos,
                key=(f"matr_aluno_" f"{st.session_state.form_key_matr}"),
            )

        if aluno_selecionado:
            turmas_filtradas = [
                turma
                for turma in lista_turmas
                if turma.curso_id == aluno_selecionado.curso_id
            ]
        else:
            turmas_filtradas = []

        with colTurma:
            turma_selecionada = st.selectbox(
                "Turma *",
                options=turmas_filtradas,
                format_func=(
                    lambda turma: (f"{turma.codigo} - {turma.disciplina.nome}")
                ),
                index=None,
                placeholder=(
                    "Selecione uma turma..."
                    if aluno_selecionado
                    else "Selecione o Aluno primeiro"
                ),
                disabled=not aluno_selecionado,
                help=(
                    "A disciplina da turma deve pertencer ao " "mesmo curso do aluno."
                ),
                key=(f"matr_turma_" f"{st.session_state.form_key_matr}"),
            )

        cadastrar = renderizarBotaoCadastro(
            rotulo="Matricular aluno",
            icone=":material/assignment_add:",
            chave=(f"btn_cad_matr_" f"{st.session_state.form_key_matr}"),
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
                    aprovacao=None,
                )

                criarMatricula(
                    matricula=nova_matricula,
                    aluno=aluno_selecionado,
                    disciplina=turma_selecionada.disciplina,
                )

                st.session_state.form_key_matr += 1
                st.session_state["cadastro_matr_realizado"] = True
                st.session_state.pop("cache_turmas", None)
                st.rerun()

            except SQLAlchemyError as erro:
                st.error("Erro ao salvar os dados no banco: " f"{erro}")

            except Exception as erro:
                st.error(str(erro))
