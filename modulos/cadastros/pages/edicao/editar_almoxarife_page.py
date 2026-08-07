from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
import re
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
from modulos.academico.academico_service import listarAlmoxarifeId, editarPessoa

def telaEdicaoAlmoxarife():
    if "ADMIN" not in st.session_state.roles:
        st.error("Acesso negado. Apenas administradores podem editar registros.")
        st.stop()

    almoxarife_id = st.session_state.get("edicao_almoxarife_id")
    if not almoxarife_id:
        st.error("Almoxarife não especificado para edição.")
        if st.button("Voltar"):
            from modulos.rotas import view_almoxarife_page
            st.switch_page(view_almoxarife_page)
        st.stop()

    almoxarife = listarAlmoxarifeId(almoxarife_id)
    if not almoxarife:
        st.error("Almoxarife não encontrado.")
        st.stop()

    if "form_key_edit_almoxarife" not in st.session_state:
        st.session_state.form_key_edit_almoxarife = 0

    col1, _ = st.columns([1, 6])
    with col1:
        if st.button(":material/arrow_back: Voltar", width="stretch"):
            st.session_state["consulta_almoxarife_id"] = almoxarife_id
            from modulos.rotas import view_almoxarife_page
            st.switch_page(view_almoxarife_page)

    st.title(":material/edit: Editar Almoxarife")
    st.caption("Altere os dados pessoais do almoxarife.")

    if st.session_state.pop("edicao_realizada", False):
        st.toast("Dados do almoxarife atualizados com sucesso!", icon=":material/check:")

    with st.container():
        with st.container():
            st.subheader("Dados Pessoais")
            with st.container(horizontal=True):
                nome = st.text_input(
                    "Nome Completo *",
                    value=almoxarife.pessoa.nome,
                    key=f"edit_almoxarife_nome_{st.session_state.form_key_edit_almoxarife}"
                )
                email = st.text_input(
                    "E-mail *",
                    value=almoxarife.pessoa.email,
                    key=f"edit_almoxarife_email_{st.session_state.form_key_edit_almoxarife}"
                )

            with st.container(horizontal=True):
                cpf = st.text_input(
                    "CPF (Somente Leitura)",
                    value=almoxarife.pessoa.cpf,
                    disabled=True,
                    key=f"edit_almoxarife_cpf_{st.session_state.form_key_edit_almoxarife}"
                )
                telefone = st.text_input(
                    "Telefone",
                    value=almoxarife.pessoa.telefone if almoxarife.pessoa.telefone else "",
                    key=f"edit_almoxarife_telefone_{st.session_state.form_key_edit_almoxarife}"
                )

            st.subheader("Vínculo Institucional")
            with st.container(horizontal=True):
                st.text_input(
                    "Campus",
                    value=almoxarife.campus.nome if almoxarife.campus else "",
                    disabled=True,
                    help="O campus do almoxarife não pode ser alterado diretamente.",
                    key=f"edit_almoxarife_campus_{st.session_state.form_key_edit_almoxarife}"
                )

        st.write("")
        _, centro, _ = st.columns([2, 3, 2])

        with centro:
            salvar = st.button(
                "Salvar Alterações",
                width="stretch",
                type="primary",
                key=f"btn_edit_almoxarife_{st.session_state.form_key_edit_almoxarife}"
            )

    if salvar:
        if not nome.strip() or not email.strip():
            st.error("Preencha todos os campos obrigatórios (Nome e E-mail).")
        else:
            try:
                editarPessoa(
                    idPessoa=almoxarife.pessoa_id,
                    nome=nome.strip(),
                    email=email.strip(),
                    telefone=telefone.strip() if telefone.strip() else None
                )
                st.session_state.form_key_edit_almoxarife += 1 
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(f"{str(e)}")
