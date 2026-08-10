import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from modulos.compras.compras_service import ( editarFornecedor, listarFornecedorId)
from modulos.utils.cadastro_visual import (marcarAcoesCadastro, marcarPainelCadastro, renderizarCabecalhoFormulario, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro)

# Tela de edição para Fornecedores
def telaEdicaoFornecedor():
    if "ADMIN" not in st.session_state.roles:
        st.error("Acesso negado. Apenas administradores podem " "editar registros.")
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

    # Função para voltar à página de visualização
    def voltarView():
        st.session_state["consulta_fornecedor_id"] = fornecedor_id
        from modulos.rotas import view_fornecedor_page

        st.switch_page(view_fornecedor_page)

    renderizarTopoCadastro(
        titulo="Editar fornecedor",
        descricao="Atualize os dados comerciais e de contato do fornecedor.",
        aoVoltar=voltarView,
        prefixoChave="edicao_fornecedor",
        categoria="EDIÇÃO",
    )

    if st.session_state.pop("edicao_realizada", False):
        st.toast(
            "Dados do fornecedor atualizados com sucesso!",
            icon=":material/check:",
        )

    with st.container(border=True):
        marcarPainelCadastro()

        renderizarCabecalhoFormulario(
            titulo=f"Editando {fornecedor.nome}",
            descricao=(
                "Revise a identificação comercial e os canais de " "atendimento."
            ),
            contexto="EDITANDO REGISTRO",
        )

        renderizarSecaoCadastro(
            numero=1,
            titulo="Informações básicas",
            descricao="Identificação legal e nome do fornecedor.",
        )

        colNome, colCnpj = st.columns([1.25, 1])

        with colNome:
            nome = st.text_input(
                "Nome do fornecedor *",
                value=fornecedor.nome,
                key=(
                    f"edit_fornecedor_nome_"
                    f"{st.session_state.form_key_edit_fornecedor}"
                ),
            )

        with colCnpj:
            st.text_input(
                "CNPJ",
                value=fornecedor.cnpj,
                disabled=True,
                help=("O CNPJ é o identificador único e não pode " "ser alterado."),
                key=(
                    f"edit_fornecedor_cnpj_"
                    f"{st.session_state.form_key_edit_fornecedor}"
                ),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Informações de contato",
            descricao="Canais utilizados na comunicação comercial.",
        )

        colEmail, colTelefone = st.columns([1.25, 1])

        with colEmail:
            email = st.text_input(
                "E-mail de contato *",
                value=fornecedor.email,
                key=(
                    f"edit_fornecedor_email_"
                    f"{st.session_state.form_key_edit_fornecedor}"
                ),
            )

        with colTelefone:
            telefone = st.text_input(
                "Telefone",
                value=fornecedor.telefone or "",
                key=(
                    f"edit_fornecedor_telefone_"
                    f"{st.session_state.form_key_edit_fornecedor}"
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
                key=(
                    f"btn_edit_fornecedor_"
                    f"{st.session_state.form_key_edit_fornecedor}"
                ),
            )

    if salvar:
        if not nome.strip() or not email.strip():
            st.error("Preencha todos os campos obrigatórios " "(Nome e E-mail).")

        else:
            try:
                editarFornecedor(
                    idFornecedor=fornecedor.id,
                    nome=nome.strip(),
                    email=email.strip(),
                    telefone=(telefone.strip() if telefone.strip() else None),
                )

                st.session_state.form_key_edit_fornecedor += 1
                st.session_state["edicao_realizada"] = True
                st.rerun()

            except SQLAlchemyError as erro:
                st.error("Erro ao salvar os dados no banco: " f"{erro}")

            except Exception as erro:
                st.error(str(erro))
