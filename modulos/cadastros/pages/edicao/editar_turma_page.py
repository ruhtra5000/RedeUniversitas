from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from modulos.academico.academico_service import listarTurmaId, alterarProfessorTurma, listarProfessoresCampus

def telaEdicaoTurma():
    if "ADMIN" not in st.session_state.roles:
        st.error("Acesso negado. Apenas administradores podem editar registros.")
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

    col1, _ = st.columns([1, 6])
    with col1:
        if st.button(":material/arrow_back: Voltar", width="stretch"):
            st.session_state["consulta_turma_id"] = turma_id
            from modulos.rotas import view_turma_page
            st.switch_page(view_turma_page)

    titulo_turma = turma.codigo or f"Turma {turma.id}"
    st.title(":material/edit: Editar Turma")
    st.caption(f"Altere o professor responsável da {titulo_turma}.")

    if st.session_state.pop("edicao_realizada", False):
        st.toast("Dados da turma atualizados com sucesso!", icon=":material/check:")

    with st.container():
        with st.container():
            st.subheader("Vínculo de Ensino")
            
            # Professores do mesmo campus
            professores = listarProfessoresCampus(turma.curso.campus_id)
            opcoes_professores = {
                prof.pessoa_id: f"{prof.pessoa.nome} - ID: {prof.pessoa_id}"
                for prof in professores
            }

            if not opcoes_professores:
                st.warning("Não há professores ativos registrados no campus deste curso para alocação.")
            else:
                try:
                    index_prof_atual = list(opcoes_professores.keys()).index(turma.professor_id)
                except ValueError:
                    # Se o professor atual não está na lista de ativos/mesmo campus, insere ele temporariamente para exibição
                    opcoes_professores[turma.professor_id] = f"{turma.professor.pessoa.nome} (Atual/Inativo/Outro Campus) - ID: {turma.professor_id}"
                    index_prof_atual = list(opcoes_professores.keys()).index(turma.professor_id)

                novo_professor_id = st.selectbox(
                    "Professor Responsável *",
                    options=list(opcoes_professores.keys()),
                    format_func=lambda x: opcoes_professores[x],
                    index=index_prof_atual,
                    key=f"edit_turma_prof_{st.session_state.form_key_edit_turma}"
                )

            st.subheader("Informações Estruturais (Somente Leitura)")
            with st.container(horizontal=True):
                st.text_input(
                    "Campus",
                    value=turma.curso.campus.nome,
                    disabled=True,
                    key=f"edit_turma_campus_{st.session_state.form_key_edit_turma}"
                )
                st.text_input(
                    "Curso",
                    value=turma.curso.nome,
                    disabled=True,
                    key=f"edit_turma_curso_{st.session_state.form_key_edit_turma}"
                )

            with st.container(horizontal=True):
                st.text_input(
                    "Disciplina",
                    value=turma.disciplina.nome,
                    disabled=True,
                    key=f"edit_turma_disciplina_{st.session_state.form_key_edit_turma}"
                )
                st.text_input(
                    "Semestre",
                    value=turma.semestre,
                    disabled=True,
                    key=f"edit_turma_semestre_{st.session_state.form_key_edit_turma}"
                )

        st.write("")
        _, centro, _ = st.columns([2, 3, 2])

        with centro:
            salvar = st.button(
                "Salvar Alterações",
                width="stretch",
                type="primary",
                key=f"btn_edit_turma_{st.session_state.form_key_edit_turma}"
            )

    if salvar:
        if not novo_professor_id:
            st.error("Selecione um professor válido.")
        else:
            try:
                if novo_professor_id != turma.professor_id:
                    alterarProfessorTurma(
                        idTurma=turma.id,
                        idNovoProfessor=novo_professor_id
                    )
                st.session_state.form_key_edit_turma += 1 
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(f"{str(e)}")
