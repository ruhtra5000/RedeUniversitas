from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from modulos.compras.compras_service import listarFornecedorId, editarFornecedor

def telaEdicaoFornecedor():
    if "ADMIN" not in st.session_state.roles:
        st.error("Acesso negado. Apenas administradores podem editar registros.")
        st.stop()

    fornecedor_id = st.session_state.get("edicao_fornecedor_id")
    if not fornecedor_id:
        st.error("Fornecedor não especificado para edição.")
        if st.button("Voltar"):
            from modulos.rotas import view_fornecedor_page
            st.switch_page(view_fornecedor_page)
        st.stop()

    fornecedor = listarFornecedorId(fornecedor_id)
    if not fornecedor:
        st.error("Fornecedor não encontrado.")
        st.stop()

    if "form_key_edit_fornecedor" not in st.session_state:
        st.session_state.form_key_edit_fornecedor = 0

    col1, _ = st.columns([1, 6])
    with col1:
        if st.button(":material/arrow_back: Voltar", width="stretch"):
            st.session_state["consulta_fornecedor_id"] = fornecedor_id
            from modulos.rotas import view_fornecedor_page
            st.switch_page(view_fornecedor_page)

    st.title(":material/edit: Editar Fornecedor")
    st.caption("Altere os dados do fornecedor.")

    if st.session_state.pop("edicao_realizada", False):
        st.toast("Dados do fornecedor atualizados com sucesso!", icon=":material/check:")

    with st.container():
        with st.container():
            st.subheader("Informações Básicas")
            with st.container(horizontal=True):
                nome = st.text_input(
                    "Nome do Fornecedor *",
                    value=fornecedor.nome,
                    key=f"edit_fornecedor_nome_{st.session_state.form_key_edit_fornecedor}"
                )
                cnpj = st.text_input(
                    "CNPJ",
                    value=fornecedor.cnpj,
                    disabled=True,
                    help="O CNPJ é o identificador único e não pode ser alterado.",
                    key=f"edit_fornecedor_cnpj_{st.session_state.form_key_edit_fornecedor}"
                )

            st.subheader("Informações de Contato")
            with st.container(horizontal=True):
                email = st.text_input(
                    "E-mail de Contato *",
                    value=fornecedor.email,
                    key=f"edit_fornecedor_email_{st.session_state.form_key_edit_fornecedor}"
                )
                telefone = st.text_input(
                    "Telefone",
                    value=fornecedor.telefone if fornecedor.telefone else "",
                    key=f"edit_fornecedor_telefone_{st.session_state.form_key_edit_fornecedor}"
                )

        st.write("")
        _, centro, _ = st.columns([2, 3, 2])

        with centro:
            salvar = st.button(
                "Salvar Alterações",
                width="stretch",
                type="primary",
                key=f"btn_edit_fornecedor_{st.session_state.form_key_edit_fornecedor}"
            )

    if salvar:
        if not nome.strip() or not email.strip():
            st.error("Preencha todos os campos obrigatórios (Nome e E-mail).")
        else:
            try:
                editarFornecedor(
                    idFornecedor=fornecedor.id,
                    nome=nome.strip(),
                    email=email.strip(),
                    telefone=telefone.strip() if telefone.strip() else None
                )
                st.session_state.form_key_edit_fornecedor += 1 
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as e:
                st.error(f"Erro ao salvar os dados no banco: {e}")
            except Exception as e:
                st.error(f"{str(e)}")
