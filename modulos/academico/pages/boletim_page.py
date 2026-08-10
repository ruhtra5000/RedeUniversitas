import pandas as pd
import streamlit as st
from modulos.academico.academico_service import (listarAlunoId, listarMatriculasAluno)
from modulos.utils.academico_visual import (marcarMetricasPagina, marcarTabelaPagina, painelPagina, renderizarTopoPagina)

# Tela de boletim do aluno
def telaBoletim():
    renderizarTopoPagina(
        titulo="Meu boletim",
        descricao=("Acompanhe seu desempenho acadêmico, suas notas " "e frequências."),
        categoria="PORTAL DO ALUNO",
    )

    pessoa_id = st.session_state.get("pessoa_id")

    if not pessoa_id:
        st.error("Erro na identificação do usuário. " "Por favor, refaça o login.")
        return

    aluno = listarAlunoId(pessoa_id)

    if not aluno:
        st.error("Nenhum vínculo de aluno foi encontrado " "para este usuário.")
        return

    with painelPagina(
        titulo="Resumo acadêmico",
        descricao="Indicadores gerais do seu vínculo como estudante.",
        contexto="VISÃO GERAL",
    ):
        colMedia, colCoeficiente, colMatricula = st.columns(3)

        with colMedia:
            marcarMetricasPagina()
            st.metric(
                label="Média geral",
                value=(
                    f"{float(aluno.media_geral):.2f}"
                    if aluno.media_geral is not None
                    else "—"
                ),
            )

        with colCoeficiente:
            st.metric(
                label="Coeficiente de rendimento",
                value=(
                    f"{float(aluno.coef_rend):.2f}"
                    if aluno.coef_rend is not None
                    else "—"
                ),
            )

        with colMatricula:
            st.metric(
                label="Registro acadêmico",
                value=aluno.matricula or "—",
            )

    matriculas = listarMatriculasAluno(pessoa_id)

    with painelPagina(
        titulo="Histórico de disciplinas",
        descricao=(
            "Notas, presença e situação de todas as disciplinas "
            "em que você possui matrícula."
        ),
        contexto="DESEMPENHO",
    ):
        if not matriculas:
            st.info(
                "Você ainda não está matriculado em nenhuma disciplina.",
                icon=":material/info:",
            )
            return

        dadosBoletim = []

        for matricula in matriculas:
            situacao = "Pendente"

            if matricula.aprovacao is True:
                situacao = "Aprovado"
            elif matricula.aprovacao is False:
                situacao = "Reprovado"

            frequencia = (
                float(matricula.frequencia_rel) * 100
                if matricula.frequencia_rel is not None
                else 0.0
            )

            dadosBoletim.append(
                {
                    "Semestre": (matricula.turma.semestre if matricula.turma else "—"),
                    "Disciplina": (
                        matricula.disciplina.nome if matricula.disciplina else "—"
                    ),
                    "Nota 1": (
                        float(matricula.nota1)
                        if matricula.nota1 not in (None, -1)
                        else None
                    ),
                    "Nota 2": (
                        float(matricula.nota2)
                        if matricula.nota2 not in (None, -1)
                        else None
                    ),
                    "Nota 3": (
                        float(matricula.nota3)
                        if matricula.nota3 not in (None, -1)
                        else None
                    ),
                    "Final": (
                        float(matricula.final)
                        if matricula.final not in (None, -1)
                        else None
                    ),
                    "Média": (
                        float(matricula.media)
                        if matricula.media not in (None, -1)
                        else None
                    ),
                    "Presenças": (
                        int(matricula.frequencia_abs)
                        if matricula.frequencia_abs is not None
                        else 0
                    ),
                    "Frequência (%)": frequencia,
                    "Situação": situacao,
                }
            )

        boletim = pd.DataFrame(dadosBoletim).sort_values(by=["Semestre", "Disciplina"])

        configuracaoColunas = {
            "Semestre": st.column_config.TextColumn("Semestre"),
            "Disciplina": st.column_config.TextColumn("Disciplina"),
            "Nota 1": st.column_config.NumberColumn("N1", format="%.1f"),
            "Nota 2": st.column_config.NumberColumn("N2", format="%.1f"),
            "Nota 3": st.column_config.NumberColumn("N3", format="%.1f"),
            "Final": st.column_config.NumberColumn("Final", format="%.1f"),
            "Média": st.column_config.NumberColumn("Média", format="%.1f"),
            "Presenças": st.column_config.NumberColumn("Presenças"),
            "Frequência (%)": st.column_config.NumberColumn(
                "Frequência",
                format="%.1f%%",
            ),
            "Situação": st.column_config.TextColumn("Situação"),
        }

        marcarTabelaPagina()

        st.dataframe(
            boletim,
            column_config=configuracaoColunas,
            width="stretch",
            hide_index=True,
        )
