from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
import re
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
from modulos.financeiro.financeiro_service import listarFinanceiroId
from modulos.academico.academico_service import editarPessoa

def telaEdicaoFinanceiro():
    if "ADMIN" not in st.session_state.roles:
        st.error("Acesso negado. Apenas administradores podem editar registros.")
        st.stop()

    financeiro_id = st.session_state.get("edicao_financeiro_id")
    if not financeiro_id:
        st.error("Membro do financeiro não especificado para edição.")
        if st.button("Voltar"):
            from modulos.rotas import view_financeiro_page
            st.switch_page(view_financeiro_page)
        st.stop()

    financeiro = listarFinanceiroId(financeiro_id)
    if not financeiro:
        st.error("Membro do financeiro não encontrado.")
        st.stop()

    if "form_key_edit_financeiro" not in st.session_state:
        st.session_state.form_key_edit_financeiro = 0

    col1, _ = st.columns([1, 6])
    with col1:
        if st.button(":material/arrow_back: Voltar", width="stretch"):
            st.session_state["consulta_financeiro_id"] = financeiro_id
            from modulos.rotas import view_financeiro_page
            st.switch_page(view_financeiro_page)

    st.title(":material/edit: Editar Financeiro")
    st.caption("Altere os dados pessoais do membro do financeiro.")

    if st.session_state.pop("edicao_realizada", False):
        st.toast("Dados atualizados com sucesso!", icon=":material/check:")

    with st.container():
        with st.container():
            st.subheader("Dados Pessoais")
            with st.container(horizontal=True):
                nome = st.text_input(
                    "Nome Completo *",
                    value=financeiro.pessoa.nome,
                    key=f"edit_financeiro_nome_{st.session_state.form_key_edit_financeiro}"
                )
                email = st.text_input(
                    "E-mail *",
                    value=financeiro.pessoa.email,
                    key=f"edit_financeiro_email_{st.session_state.form_key_edit_financeiro}"
                )

            with st.container(horizontal=True):
                cpf = st.text_input(
                    "CPF (Somente Leitura)",
                    value=financeiro.pessoa.cpf,
                    disabled=True,
                    key=f"edit_financeiro_cpf_{st.session_state.form_key_edit_financeiro}"
                )
                telefone = st.text_input(
                    "Telefone",
                    value=financeiro.pessoa.telefone if financeiro.pessoa.telefone else "",
                    key=f"edit_financeiro_telefone_{st.session_state.form_key_edit_financeiro}"
                )

            st.subheader("Vínculo Institucional")
            with st.container(horizontal=True):
                st.text_input(
                    "Campus",
                    value=financeiro.campus.nome if financeiro.campus else "",
                    disabled=True,
                    help="O campus não pode ser alterado diretamente.",
                    key=f"edit_financeiro_campus_{st.session_state.form_key_edit_financeiro}"
                )

        st.write("")
        _, centro, _ = st.columns([2, 3, 2])

        with centro:
            salvar = st.button(
                "Salvar Alterações",
                width="stretch",
                type="primary",
                key=f"btn_edit_financeiro_{st.session_state.form_key_edit_financeiro}"
            )

    if salvar:
        if not nome.strip() or not email.strip():
            st.error("Preencha todos os campos obrigatórios (Nome e E-mail).")
        else:
            try:
                editarPessoa(
                    idPessoa=financeiro.pessoa_id,
                    nome=nome.strip(),
                    email=email.strip(),
                    telefone=telefone.strip() if telefone.strip() else None
                )
                st.session_state.form_key_edit_financeiro += 1 
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(f"{str(e)}")
