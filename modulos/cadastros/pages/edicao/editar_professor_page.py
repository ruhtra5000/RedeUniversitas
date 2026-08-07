from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
import re
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
from modulos.academico.academico_service import listarProfessorId, editarPessoa

def telaEdicaoProfessor():
    if "ADMIN" not in st.session_state.roles:
        st.error("Acesso negado. Apenas administradores podem editar registros.")
        st.stop()

    professor_id = st.session_state.get("edicao_professor_id")
    if not professor_id:
        st.error("Professor não especificado para edição.")
        if st.button("Voltar"):
            from modulos.rotas import view_professor_page
            st.switch_page(view_professor_page)
        st.stop()

    professor = listarProfessorId(professor_id)
    if not professor:
        st.error("Professor não encontrado.")
        st.stop()

    if "form_key_edit_professor" not in st.session_state:
        st.session_state.form_key_edit_professor = 0

    col1, _ = st.columns([1, 6])
    with col1:
        if st.button(":material/arrow_back: Voltar", width="stretch"):
            st.session_state["consulta_professor_id"] = professor_id
            from modulos.rotas import view_professor_page
            st.switch_page(view_professor_page)

    st.title(":material/edit: Editar Professor")
    st.caption("Altere os dados pessoais do professor.")

    if st.session_state.pop("edicao_realizada", False):
        st.toast("Dados do professor atualizados com sucesso!", icon=":material/check:")

    with st.container():
        with st.container():
            st.subheader("Dados Pessoais")
            with st.container(horizontal=True):
                nome = st.text_input(
                    "Nome Completo *",
                    value=professor.pessoa.nome,
                    key=f"edit_professor_nome_{st.session_state.form_key_edit_professor}"
                )
                email = st.text_input(
                    "E-mail *",
                    value=professor.pessoa.email,
                    key=f"edit_professor_email_{st.session_state.form_key_edit_professor}"
                )

            with st.container(horizontal=True):
                cpf = st.text_input(
                    "CPF (Somente Leitura)",
                    value=professor.pessoa.cpf,
                    disabled=True,
                    key=f"edit_professor_cpf_{st.session_state.form_key_edit_professor}"
                )
                telefone = st.text_input(
                    "Telefone",
                    value=professor.pessoa.telefone if professor.pessoa.telefone else "",
                    key=f"edit_professor_telefone_{st.session_state.form_key_edit_professor}"
                )

            st.subheader("Vínculo Institucional")
            with st.container(horizontal=True):
                st.text_input(
                    "Campus",
                    value=professor.campus.nome if professor.campus else "",
                    disabled=True,
                    help="O campus do professor não pode ser alterado diretamente.",
                    key=f"edit_professor_campus_{st.session_state.form_key_edit_professor}"
                )

        st.write("")
        _, centro, _ = st.columns([2, 3, 2])

        with centro:
            salvar = st.button(
                "Salvar Alterações",
                width="stretch",
                type="primary",
                key=f"btn_edit_professor_{st.session_state.form_key_edit_professor}"
            )

    if salvar:
        if not nome.strip() or not email.strip():
            st.error("Preencha todos os campos obrigatórios (Nome e E-mail).")
        else:
            try:
                editarPessoa(
                    idPessoa=professor.pessoa_id,
                    nome=nome.strip(),
                    email=email.strip(),
                    telefone=telefone.strip() if telefone.strip() else None
                )
                st.session_state.form_key_edit_professor += 1 
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(f"{str(e)}")
