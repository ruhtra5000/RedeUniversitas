import streamlit as st

from modulos.estoque.estoque_service import listarProdutoId
from modulos.utils.view_utils import exibirCampo, formatar_situacao_estoque, limpar_consulta_produto

# Tela de visualização de produto
def telaViewProduto():

    st.title(":material/search: Consulta de Produto")
    st.caption("Pesquise um produto pelo ID.")

    selecionado = st.session_state.pop("produto_selecionado", None)

    if selecionado is not None:
        st.session_state["consulta_produto_id"] = (
            selecionado
        )

    produto = None
    erro_consulta = False

    col_voltar, _ = st.columns([1, 5])

    with col_voltar:
        if st.button(
            ":material/arrow_back: Voltar",
            use_container_width=True,
        ):
            from modulos.rotas import listagem_produto_page
            st.switch_page(listagem_produto_page)

    with st.form("buscar_produto", border=True):

        st.markdown("#### :material/search: Buscar produto")

        id_digitado = st.text_input(
            "ID",
            placeholder="Ex.: 1",
            key="consulta_produto_id_digitado",
        )

        coluna_botao, _ = st.columns([1.3, 4.7])

        with coluna_botao:
            buscar = st.form_submit_button(
                ":material/search: Buscar",
                type="primary",
                use_container_width=True,
            )

    if buscar:
        st.session_state.pop(
            "consulta_produto_id",
            None,
        )

        id_produto = id_digitado.strip()

        if not id_produto:
            st.warning("Informe o ID do produto.")

        elif not id_produto.isdigit():
            st.error(
                "O ID deve conter somente números."
            )

        else:
            try:
                produto = listarProdutoId(
                    int(id_produto)
                )

                if produto is None:
                    st.error("Produto não encontrado.")

                else:
                    st.session_state["consulta_produto_id"] = produto.id

            except Exception as erro:
                erro_consulta = True
                st.error(str(erro))

    produto_id = st.session_state.get(
        "consulta_produto_id"
    )

    if produto is None and produto_id is not None:
        try:
            produto = listarProdutoId(produto_id)

            if produto is None:
                erro_consulta = True

                st.session_state.pop("consulta_produto_id", None)

                st.error("Produto não encontrado.")

        except Exception as erro:
            erro_consulta = True

            st.session_state.pop("consulta_produto_id", None)

            st.error(str(erro))

    if produto is None:
        if not buscar and not erro_consulta:
            st.info(
                "Informe um ID para consultar um produto."
            )

        return

    st.write("")

    titulo, botao = st.columns(
        [4.7, 1.3],
        vertical_alignment="center",
    )

    with titulo:
        st.subheader(f":material/inventory_2: {produto.nome}")

    with botao:
        st.button(
            "Limpar",
            icon=":material/close:",
            use_container_width=True,
            on_click=limpar_consulta_produto,
        )

    with st.container(border=True):

        st.markdown("#### :material/inventory_2: Dados do Produto")

        col1, col2, col3 = st.columns(
            [1, 3, 2]
        )

        altura_dados = 110

        with col1:
            exibirCampo(
                "ID",
                produto.id,
                altura=altura_dados,
            )

        with col2:
            exibirCampo(
                "Produto",
                produto.nome,
                altura=altura_dados,
            )

        with col3:
            exibirCampo(
                "Marca",
                produto.marca or "Não informada",
                altura=altura_dados,
            )

    st.write("")

    with st.container(border=True):

        st.markdown("#### :material/account_balance: Controle de Estoque")

        col1, col2, col3 = st.columns(3)

        altura_estoque = 120

        with col1:
            exibirCampo(
                "Campus",
                produto.campus.nome
                if produto.campus
                else "Não informado",
                altura=altura_estoque,
            )

        with col2:
            exibirCampo(
                "Quantidade atual",
                produto.qtde,
                altura=altura_estoque,
            )

        with col3:
            exibirCampo(
                "Quantidade mínima",
                produto.qtde_min,
                altura=altura_estoque,
            )

        st.write("")

        exibirCampo(
            "Situação",
            formatar_situacao_estoque(produto),
        )