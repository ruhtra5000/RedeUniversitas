from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from modulos.academico.academico_service import listarDisciplinaId, editarDisciplina

def telaEdicaoDisciplina():
    if "ADMIN" not in st.session_state.roles:
        st.error("Acesso negado. Apenas administradores podem editar registros.")
        st.stop()

    disciplina_id = st.session_state.get("edicao_disciplina_id")
    if not disciplina_id:
        st.error("Disciplina não especificada para edição.")
        if st.button("Voltar"):
            from modulos.rotas import view_disciplina_page
            st.switch_page(view_disciplina_page)
        st.stop()

    disciplina = listarDisciplinaId(disciplina_id)
    if not disciplina:
        st.error("Disciplina não encontrada.")
        st.stop()

    if "form_key_edit_disciplina" not in st.session_state:
        st.session_state.form_key_edit_disciplina = 0

    col1, _ = st.columns([1, 6])
    with col1:
        if st.button(":material/arrow_back: Voltar", width="stretch"):
            st.session_state["consulta_disciplina_id"] = disciplina_id
            from modulos.rotas import view_disciplina_page
            st.switch_page(view_disciplina_page)

    st.title(":material/edit: Editar Disciplina")
    st.caption("Altere os dados da disciplina.")

    if st.session_state.pop("edicao_realizada", False):
        st.toast("Dados da disciplina atualizados com sucesso!", icon=":material/check:")

    with st.container():
        with st.container():
            st.subheader("Informações Básicas")
            with st.container(horizontal=True):
                nome = st.text_input(
                    "Nome da Disciplina *",
                    value=disciplina.nome,
                    key=f"edit_disciplina_nome_{st.session_state.form_key_edit_disciplina}"
                )
                
            with st.container(horizontal=True):
                carga_horaria = st.number_input(
                    "Carga Horária Total (h)",
                    min_value=1,
                    value=disciplina.carga_horaria,
                    disabled=True,
                    help="A carga horária não pode ser alterada para evitar inconsistências em mensalidades.",
                    key=f"edit_disciplina_carga_horaria_{st.session_state.form_key_edit_disciplina}"
                )
                
                obrigatoria = st.checkbox(
                    "Disciplina Obrigatória",
                    value=disciplina.obrigatoria,
                    key=f"edit_disciplina_obrigatoria_{st.session_state.form_key_edit_disciplina}"
                )

            st.subheader("Vínculo Institucional")
            st.text_input(
                "Curso",
                value=disciplina.curso.nome if disciplina.curso else "",
                disabled=True,
                help="O curso da disciplina não pode ser alterado diretamente.",
                key=f"edit_disciplina_curso_{st.session_state.form_key_edit_disciplina}"
            )

        st.write("")
        _, centro, _ = st.columns([2, 3, 2])

        with centro:
            salvar = st.button(
                "Salvar Alterações",
                width="stretch",
                type="primary",
                key=f"btn_edit_disciplina_{st.session_state.form_key_edit_disciplina}"
            )

    if salvar:
        if not nome.strip():
            st.error("Preencha o Nome da Disciplina.")
        else:
            try:
                editarDisciplina(
                    idDisciplina=disciplina.id,
                    nome=nome.strip(),
                    carga_horaria=disciplina.carga_horaria, # Always use the existing value
                    obrigatoria=obrigatoria
                )
                st.session_state.form_key_edit_disciplina += 1 
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(f"{str(e)}")
