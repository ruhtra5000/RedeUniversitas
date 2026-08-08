import re
import streamlit as st
from modulos.compras.compras_service import listarFornecedorId
from modulos.utils.view_utils import exibirCampo, formatar_cnpj, limpar_consulta_fornecedor

# Tela de visualização de fornecedor
def telaViewFornecedor():

    st.title(":material/search: Consulta de Fornecedor")
    st.caption("Pesquise um fornecedor pelo ID.")

    selecionado = st.session_state.pop("fornecedor_selecionado", None)

    if selecionado is not None:
        st.session_state[
            "consulta_fornecedor_id"
        ] = selecionado

    fornecedor = None
    erro_consulta = False

    col_voltar, _ = st.columns([1, 5])

    with col_voltar:
        if st.button(
            ":material/arrow_back: Voltar",
            use_container_width=True,
        ):
            pass

    with st.form("buscar_fornecedor", border=True):

        st.markdown("#### :material/search: Buscar fornecedor")

        id_digitado = st.text_input(
            "ID",
            placeholder="Ex.: 1",
            key="consulta_fornecedor_id_digitado",
        )

        coluna_botao, _ = st.columns([1.3, 4.7])

        with coluna_botao:
            buscar = st.form_submit_button(
                ":material/search: Buscar",
                type="primary",
                use_container_width=True,
            )

    if buscar:
        st.session_state.pop("consulta_fornecedor_id", None)

        id_fornecedor = id_digitado.strip()

        if not id_fornecedor:
            st.warning("Informe o ID do fornecedor.")

        elif not id_fornecedor.isdigit():
            st.error(
                "O ID deve conter somente números."
            )

        else:
            try:
                fornecedor = listarFornecedorId(
                    int(id_fornecedor)
                )

                if fornecedor is None:
                    st.error(
                        "Fornecedor não encontrado."
                    )

                else:
                    st.session_state["consulta_fornecedor_id"] = fornecedor.id

            except Exception as erro:
                erro_consulta = True
                st.error(str(erro))

    fornecedor_id = st.session_state.get(
        "consulta_fornecedor_id"
    )

    if fornecedor is None and fornecedor_id is not None:
        try:
            fornecedor = listarFornecedorId(
                fornecedor_id
            )

            if fornecedor is None:
                erro_consulta = True

                st.session_state.pop("consulta_fornecedor_id", None)

                st.error("Fornecedor não encontrado.")

        except Exception as erro:
            erro_consulta = True

            st.session_state.pop("consulta_fornecedor_id", None)

            st.error(str(erro))

    if fornecedor is None:
        if not buscar and not erro_consulta:
            st.info(
                "Informe um ID para consultar um fornecedor."
            )

        return

    st.write("")

    titulo, botao_limpar, botao_editar = st.columns(
        [4.2, 0.9, 0.9],
        vertical_alignment="center",
    )

    with titulo:
        st.subheader(f":material/factory: {fornecedor.nome}")

    with botao_limpar:
        st.button(
            "Limpar",
            icon=":material/close:",
            use_container_width=True,
            on_click=limpar_consulta_fornecedor,
        )

    with botao_editar:
        if "ADMIN" in st.session_state.roles:
            if st.button(
                "Editar",
                icon=":material/edit:",
                use_container_width=True,
                type="secondary"
            ):
                st.session_state["edicao_fornecedor_id"] = fornecedor.id
                from modulos.rotas import editar_fornecedor_page
                st.switch_page(editar_fornecedor_page)

    with st.container(border=True):

        st.markdown("#### :material/factory: Dados do Fornecedor")

        col1, col2, col3 = st.columns(
            [1, 3, 2]
        )

        altura_dados = 115

        with col1:
            exibirCampo(
                "ID",
                fornecedor.id,
                altura=altura_dados,
            )

        with col2:
            exibirCampo(
                "Fornecedor",
                fornecedor.nome,
                altura=altura_dados,
            )

        with col3:
            exibirCampo(
                "CNPJ",
                formatar_cnpj(fornecedor.cnpj),
                altura=altura_dados,
            )

    st.write("")

    with st.container(border=True):

        st.markdown("#### :material/call: Informações de Contato")

        col1, col2 = st.columns(2)

        altura_contato = 110

        with col1:
            exibirCampo(
                "E-mail",
                fornecedor.email
                or "Não informado",
                altura=altura_contato,
            )

        with col2:
            exibirCampo(
                "Telefone",
                fornecedor.telefone
                or "Não informado",
                altura=altura_contato,
            )