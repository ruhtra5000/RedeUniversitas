from decimal import Decimal
import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from modulos.academico.academico_service import (cadastrarPresenca, fecharTurma, lancarNota1, lancarNota2, lancarNota3, lancarNotaFinal, listarTurmasGeral)
from modulos.utils.academico_visual import (marcarAcoesPagina, marcarTabelaPagina, painelPagina, renderizarTopoPagina)

# Tela de diário de classe do professor
def telaDiarioClasse():
    renderizarTopoPagina(
        titulo="Diário de classe",
        descricao=(
            "Registre notas e presenças e consolide o resultado " "das suas turmas."
        ),
        categoria="PORTAL DO PROFESSOR",
    )

    if st.session_state.pop("diario_salvo", False):
        st.toast(
            "Lançamentos salvos com sucesso!",
            icon=":material/check:",
        )

    if st.session_state.pop("turma_fechada", False):
        st.toast(
            "Turma consolidada com sucesso!",
            icon=":material/check:",
        )

    if "form_key_diario" not in st.session_state:
        st.session_state.form_key_diario = 0

    if "cache_turmas" not in st.session_state:
        st.session_state.cache_turmas = listarTurmasGeral()

    listaTurmas = st.session_state.cache_turmas
    pessoa_id = st.session_state.get("pessoa_id")
    turmasProfessor = [
        turma for turma in listaTurmas if turma.professor_id == pessoa_id
    ]

    with painelPagina(
        titulo="Selecionar turma",
        descricao="Escolha uma de suas turmas para abrir o diário.",
        contexto="TURMAS ATRIBUÍDAS",
    ):
        turmaSelecionada = st.selectbox(
            "Sua turma",
            options=turmasProfessor,
            format_func=lambda turma: (
                f"{turma.semestre} | {turma.codigo} — " f"{turma.disciplina.nome}"
            ),
            index=None,
            placeholder=(
                "Selecione uma turma..."
                if turmasProfessor
                else "Nenhuma turma atribuída a você."
            ),
            disabled=not turmasProfessor,
            key="diario_turma",
        )

    if not turmaSelecionada:
        return

    turma = next(
        (item for item in listaTurmas if item.id == turmaSelecionada.id),
        None,
    )

    if not turma:
        return

    matriculas = turma.matriculas

    with painelPagina(
        titulo=f"Lançamentos — {turma.disciplina.nome}",
        descricao=(
            "Edite notas e adicione presenças diretamente na tabela. "
            "Os demais campos são calculados pelo sistema."
        ),
        contexto=f"TURMA {turma.codigo}",
    ):
        if not matriculas:
            st.info("Nenhum aluno está matriculado nesta turma.")
            return

        dadosOriginais = []

        for matricula in matriculas:
            situacao = "Pendente"

            if matricula.aprovacao is True:
                situacao = "Aprovado"
            elif matricula.aprovacao is False:
                situacao = "Reprovado"

            totalAulas = int(turma.disciplina.carga_horaria * 0.75)

            dadosOriginais.append(
                {
                    "ID Aluno": matricula.aluno_id,
                    "Nome": matricula.aluno.pessoa.nome,
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
                    "Total Aulas": totalAulas,
                    "Frequência %": (
                        f"{matricula.frequencia_rel}%"
                        if matricula.frequencia_rel is not None
                        else "0.0%"
                    ),
                    "Situação": situacao,
                    "Adicionar Presenças": 0,
                }
            )

        marcarTabelaPagina()

        dadosEditados = st.data_editor(
            dadosOriginais,
            disabled=[
                "ID Aluno",
                "Nome",
                "Média",
                "Presenças",
                "Total Aulas",
                "Frequência %",
                "Situação",
            ],
            hide_index=True,
            width="stretch",
            column_config={
                "ID Aluno": None,
                "Nota 1": st.column_config.NumberColumn(
                    min_value=0.0,
                    max_value=10.0,
                    step=0.1,
                    format="%.1f",
                ),
                "Nota 2": st.column_config.NumberColumn(
                    min_value=0.0,
                    max_value=10.0,
                    step=0.1,
                    format="%.1f",
                ),
                "Nota 3": st.column_config.NumberColumn(
                    min_value=0.0,
                    max_value=10.0,
                    step=0.1,
                    format="%.1f",
                ),
                "Final": st.column_config.NumberColumn(
                    min_value=0.0,
                    max_value=10.0,
                    step=0.1,
                    format="%.1f",
                ),
                "Média": st.column_config.NumberColumn(format="%.1f"),
                "Adicionar Presenças": st.column_config.NumberColumn(
                    min_value=0,
                    max_value=100,
                    step=1,
                ),
            },
            key=(f"editor_turma_{turma.id}_" f"{st.session_state.form_key_diario}"),
        )

        marcarAcoesPagina()
        colSalvar, _, colConsolidar = st.columns([1, 1, 1])

        with colSalvar:
            salvar = st.button(
                "Salvar lançamentos",
                icon=":material/save:",
                type="primary",
                width="stretch",
            )

        with colConsolidar:
            consolidar = st.button(
                "Consolidar turma",
                icon=":material/lock:",
                width="stretch",
                help=("Calcula a situação final dos alunos e " "fecha a turma."),
            )

        if salvar:
            try:
                for original, editado in zip(
                    dadosOriginais,
                    dadosEditados,
                ):
                    aluno_id = original["ID Aluno"]

                    if (
                        editado["Nota 1"] != original["Nota 1"]
                        and editado["Nota 1"] is not None
                    ):
                        lancarNota1(
                            aluno_id,
                            turma.id,
                            Decimal(str(editado["Nota 1"])),
                        )

                    if (
                        editado["Nota 2"] != original["Nota 2"]
                        and editado["Nota 2"] is not None
                    ):
                        lancarNota2(
                            aluno_id,
                            turma.id,
                            Decimal(str(editado["Nota 2"])),
                        )

                    if (
                        editado["Nota 3"] != original["Nota 3"]
                        and editado["Nota 3"] is not None
                    ):
                        lancarNota3(
                            aluno_id,
                            turma.id,
                            Decimal(str(editado["Nota 3"])),
                        )

                    if (
                        editado["Final"] != original["Final"]
                        and editado["Final"] is not None
                    ):
                        lancarNotaFinal(
                            aluno_id,
                            turma.id,
                            Decimal(str(editado["Final"])),
                        )

                    if editado.get("Adicionar Presenças", 0) > 0:
                        cadastrarPresenca(
                            aluno_id,
                            turma.id,
                            int(editado["Adicionar Presenças"]),
                        )

                st.session_state["diario_salvo"] = True
                st.session_state.pop("cache_turmas", None)
                st.session_state.form_key_diario += 1
                st.rerun()

            except SQLAlchemyError as erro:
                st.error(f"Erro no banco de dados: {erro}")

            except Exception as erro:
                st.error(f"Ocorreu um erro ao salvar: {erro}")

        if consolidar:
            try:
                fecharTurma(turma.id)
                st.session_state["turma_fechada"] = True
                st.session_state.pop("cache_turmas", None)
                st.session_state.form_key_diario += 1
                st.rerun()

            except SQLAlchemyError as erro:
                st.error(f"Erro no banco de dados: {erro}")

            except Exception as erro:
                st.error(f"Ocorreu um erro ao consolidar a turma: {erro}")
