import time
from decimal import Decimal
import streamlit as st
from database.entidades.Matricula import Matricula
from modulos.academico.academico_service import (listarAlunoId, listarTurmasDisponiveisAluno,)
from modulos.cadastros.matricula import criarMatricula
from modulos.utils.academico_visual import (marcarAcoesPagina, painelPagina, renderizarDivisorPagina, renderizarSecaoPagina, renderizarTopoPagina)

@st.dialog("Confirmação da matrícula")
def modalConfirmacao(aluno, turmasSelecionadas):
    st.caption("Revise as disciplinas antes de confirmar a sua matrícula.")

    for turma in turmasSelecionadas:
        st.write(f"• **{turma.disciplina.nome}** " f"— Turma {turma.codigo}")

    colConfirmar, colCancelar = st.columns(2)

    with colConfirmar:
        confirmar = st.button(
            "Confirmar",
            icon=":material/check:",
            type="primary",
            width="stretch",
        )

    with colCancelar:
        cancelar = st.button(
            "Cancelar",
            icon=":material/close:",
            width="stretch",
        )

    if confirmar:
        sucesso = True

        with st.spinner("Efetivando matrículas..."):
            for turma in turmasSelecionadas:
                try:
                    novaMatricula = Matricula(
                        aluno_id=aluno.pessoa_id,
                        turma_id=turma.id,
                        disciplina_id=turma.disciplina_id,
                        nota1=Decimal("-1.00"),
                        nota2=Decimal("-1.00"),
                        nota3=Decimal("-1.00"),
                        final=Decimal("-1.00"),
                        media=Decimal("0.00"),
                        frequencia_abs=0,
                        frequencia_rel=Decimal("0.00"),
                        aprovacao=False,
                    )

                    criarMatricula(
                        novaMatricula,
                        aluno,
                        turma.disciplina,
                    )

                except Exception as erro:
                    st.error(f"Erro ao matricular na turma {turma.codigo}: " f"{erro}")
                    sucesso = False

        if sucesso:
            st.success("Matrículas efetivadas com sucesso!")
            time.sleep(1.5)
            st.rerun()

    if cancelar:
        st.rerun()

# Tela de renovação de matrícula do aluno
def telaRenovarMatricula():
    renderizarTopoPagina(
        titulo="Renovar matrícula",
        descricao=(
            "Selecione as disciplinas disponíveis para o seu curso "
            "e confirme sua inscrição."
        ),
        categoria="PORTAL DO ALUNO",
    )

    roles = st.session_state.get("roles", [])

    if "ALUNO" not in roles:
        st.error("Acesso negado. Apenas alunos podem acessar esta página.")
        return

    pessoa_id = st.session_state.get("pessoa_id")

    if not pessoa_id:
        st.error("Sessão inválida. Por favor, refaça o login.")
        return

    try:
        aluno = listarAlunoId(pessoa_id)

    except Exception as erro:
        st.error(f"Erro ao carregar dados do aluno: {erro}")
        return

    turmasValidas = listarTurmasDisponiveisAluno(pessoa_id)

    with painelPagina(
        titulo="Inscrição acadêmica",
        descricao=(
            "Confira seu vínculo e selecione as novas turmas " "para o período."
        ),
        contexto="RENOVAÇÃO",
    ):
        renderizarSecaoPagina(
            numero=1,
            titulo="Vínculo atual",
            descricao="Aluno e curso associados à sessão.",
        )

        colAluno, colCurso = st.columns(2)

        with colAluno:
            st.text_input(
                "Aluno",
                value=aluno.pessoa.nome,
                disabled=True,
            )

        with colCurso:
            st.text_input(
                "Curso",
                value=aluno.curso.nome,
                disabled=True,
            )

        renderizarDivisorPagina()

        renderizarSecaoPagina(
            numero=2,
            titulo="Disciplinas disponíveis",
            descricao=(
                "Somente turmas compatíveis com seu curso e "
                "pré-requisitos são exibidas."
            ),
        )

        if not turmasValidas:
            st.info(
                "Não há turmas disponíveis no momento. Você pode já ter "
                "concluído as disciplinas possíveis ou ainda não possuir "
                "os pré-requisitos necessários."
            )
            return

        turmasSelecionadas = st.multiselect(
            "Turmas disponíveis",
            options=turmasValidas,
            format_func=lambda turma: (
                f"{turma.disciplina.nome} — " f"Turma {turma.codigo} | {turma.semestre}"
            ),
            placeholder="Selecione uma ou mais turmas...",
        )

        marcarAcoesPagina()

        _, colunaBotao, _ = st.columns([2, 3, 2])

        with colunaBotao:
            confirmar = st.button(
                "Confirmar inscrição",
                icon=":material/how_to_reg:",
                type="primary",
                width="stretch",
                disabled=not turmasSelecionadas,
            )

        if confirmar:
            modalConfirmacao(aluno, turmasSelecionadas)
