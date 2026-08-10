import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from modulos.academico.academico_service import (alterarProfessorTurma, listarProfessoresCampus, listarTurmaId)
from modulos.utils.cadastro_visual import (marcarAcoesCadastro, marcarPainelCadastro, renderizarAvisoCadastro, renderizarCabecalhoFormulario, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro, aplicarEstiloCamposBloqueados)

# Tela de edição para Turmas
def telaEdicaoTurma():

    aplicarEstiloCamposBloqueados()

    if "ADMIN" not in st.session_state.roles:
        st.error(
            "Acesso negado. Apenas administradores podem "
            "editar registros."
        )
        st.stop()

    turma_id = st.session_state.get("edicao_turma_id")

    if not turma_id:
        st.error("Turma não especificada para edição.")

        if st.button("Voltar"):
            from modulos.rotas import view_turma_page
            st.switch_page(view_turma_page)

        st.stop()

    turma = listarTurmaId(turma_id)

    if not turma:
        st.error("Turma não encontrada.")
        st.stop()

    if "form_key_edit_turma" not in st.session_state:
        st.session_state.form_key_edit_turma = 0

    titulo_turma = turma.codigo or f"Turma {turma.id}"

    def voltarView():
        st.session_state["consulta_turma_id"] = turma_id
        from modulos.rotas import view_turma_page
        st.switch_page(view_turma_page)

    renderizarTopoCadastro(
        titulo="Editar turma",
        descricao=f"Atualize o professor responsável pela {titulo_turma}.",
        aoVoltar=voltarView,
        prefixoChave="edicao_turma",
        categoria="EDIÇÃO",
    )

    if st.session_state.pop("edicao_realizada", False):
        st.toast(
            "Dados da turma atualizados com sucesso!",
            icon=":material/check:",
        )

    professores = listarProfessoresCampus(turma.curso.campus_id)
    opcoes_professores = {
        professor.pessoa_id: (
            f"{professor.pessoa.nome} - ID: {professor.pessoa_id}"
        )
        for professor in professores
    }
    novo_professor_id = None

    with st.container(border=True):
        marcarPainelCadastro()

        renderizarCabecalhoFormulario(
            titulo=f"Editando {titulo_turma}",
            descricao=(
                "Defina o professor responsável e confira os vínculos "
                "acadêmicos da turma."
            ),
            contexto="EDITANDO REGISTRO",
        )

        renderizarSecaoCadastro(
            numero=1,
            titulo="Vínculo de ensino",
            descricao="Professor responsável pela condução da turma.",
        )

        if not opcoes_professores:
            renderizarAvisoCadastro(
                titulo="Nenhum professor disponível",
                descricao=(
                    "Não há professores ativos vinculados ao campus "
                    "deste curso."
                ),
            )

        else:
            if turma.professor_id not in opcoes_professores:
                opcoes_professores[turma.professor_id] = (
                    f"{turma.professor.pessoa.nome} "
                    "(atual, inativo ou de outro campus) - "
                    f"ID: {turma.professor_id}"
                )

            ids_professores = list(opcoes_professores.keys())
            index_prof_atual = ids_professores.index(turma.professor_id)

            novo_professor_id = st.selectbox(
                "Professor responsável *",
                options=ids_professores,
                format_func=lambda identificador: (
                    opcoes_professores[identificador]
                ),
                index=index_prof_atual,
                key=(
                    f"edit_turma_prof_"
                    f"{st.session_state.form_key_edit_turma}"
                ),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Informações estruturais",
            descricao="Vínculos acadêmicos mantidos somente para leitura.",
        )

        colCampus, colCurso = st.columns(2)

        with colCampus:
            st.text_input(
                "Campus",
                value=turma.curso.campus.nome,
                disabled=True,
                key=(
                    f"edit_turma_campus_"
                    f"{st.session_state.form_key_edit_turma}"
                ),
            )

        with colCurso:
            st.text_input(
                "Curso",
                value=turma.curso.nome,
                disabled=True,
                key=(
                    f"edit_turma_curso_"
                    f"{st.session_state.form_key_edit_turma}"
                ),
            )

        colDisciplina, colSemestre = st.columns([1.35, 1])

        with colDisciplina:
            st.text_input(
                "Disciplina",
                value=turma.disciplina.nome,
                disabled=True,
                key=(
                    f"edit_turma_disciplina_"
                    f"{st.session_state.form_key_edit_turma}"
                ),
            )

        with colSemestre:
            st.text_input(
                "Semestre",
                value=turma.semestre,
                disabled=True,
                key=(
                    f"edit_turma_semestre_"
                    f"{st.session_state.form_key_edit_turma}"
                ),
            )

        _, centro, _ = st.columns([2, 3, 2])

        with centro:
            marcarAcoesCadastro()

            salvar = st.button(
                "Salvar alterações",
                icon=":material/save:",
                width="stretch",
                type="primary",
                disabled=not opcoes_professores,
                key=(
                    f"btn_edit_turma_"
                    f"{st.session_state.form_key_edit_turma}"
                ),
            )

    if salvar:
        if not novo_professor_id:
            st.error("Selecione um professor válido.")

        else:
            try:
                if novo_professor_id != turma.professor_id:
                    alterarProfessorTurma(
                        idTurma=turma.id,
                        idNovoProfessor=novo_professor_id,
                    )

                st.session_state.form_key_edit_turma += 1
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as erro:
                st.error(
                    "Erro ao salvar os dados no banco: "
                    f"{erro}"
                )

            except Exception as erro:
                st.error(str(erro))
