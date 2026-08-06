import streamlit as st

from modulos.estoque.estoque_service import listarProdutos
from modulos.utils.listagem_utils import separador, formatar_estoque

# Tela de listagem para Produtos
def telaListagemProdutos():

    st.title("📋 Listagem de Produtos")
    st.caption("Consulte os produtos cadastrados no estoque.")

    colVoltar, _ = st.columns([1, 5])

    with colVoltar:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import home_page
            st.switch_page(home_page)

    listaProdutos = listarProdutos()

    if not listaProdutos:
        st.info("📦 Nenhum produto cadastrado.")
        return

    st.write("")

    st.caption(
        f"📦 {len(listaProdutos)} "
        f"{'produto encontrado' if len(listaProdutos) == 1 else 'produtos encontrados'}"
    )

    proporcoes = [3, 2.2, 2.5, 3, 1.3]

    with st.container(border=True):

        h1, h2, h3, h4, h5 = st.columns(
            proporcoes,
            vertical_alignment="center",
        )

        h1.markdown("**Produto**")
        h2.markdown("**Marca**")
        h3.markdown("**Estoque**")
        h4.markdown("**Campus**")
        h5.markdown("**Ações**")

        separador()

        for indice, produto in enumerate(listaProdutos):

            c1, c2, c3, c4, c5 = st.columns(
                proporcoes,
                vertical_alignment="center",
            )

            with c1:
                st.markdown(f"**{produto.nome}**")

            with c2:
                st.write(
                    produto.marca or "Não informada"
                )

            with c3:
                st.write(formatar_estoque(produto))

            with c4:
                st.write(
                    produto.campus.nome
                    if produto.campus
                    else "Não informado"
                )

            with c5:
                visualizar = st.button(
                    "👁️",
                    key=f"view_produto_{produto.id}",
                    help="Visualizar produto",
                    use_container_width=True,
                )

            if visualizar:
                st.session_state["produto_selecionado"] = produto.id

                from modulos.rotas import view_produto_page
                st.switch_page(view_produto_page)

            if indice < len(listaProdutos) - 1:
                separador()