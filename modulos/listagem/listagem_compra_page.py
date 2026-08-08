import streamlit as st
from modulos.compras.compras_service import listarCompras
from modulos.utils.listagem_utils import separador, formatar_moeda, formatar_data, obter_nome_produto

# Tela de listagem para Compras
def telaListagemCompras():

    st.title(":material/assignment: Listagem de Compras")
    st.caption("Consulte as compras cadastradas no sistema.")

    colVoltar, _ = st.columns([1, 5])

    with colVoltar:
        if st.button(":material/arrow_back: Voltar", use_container_width=True):
            from modulos.rotas import home_page
            st.switch_page(home_page)

    listaCompras = listarCompras()

    if not listaCompras:
        st.info(":material/shopping_cart: Nenhuma compra cadastrada.")
        return

    st.write("")

    st.caption(
        f":material/shopping_cart: {len(listaCompras)} "
        f"{'compra encontrada' if len(listaCompras) == 1 else 'compras encontradas'}"
    )

    proporcoes = [2.8, 2.5, 1.1, 1.8, 1.8, 1.2]

    with st.container(border=True):

        h1, h2, h3, h4, h5, h6 = st.columns(
            proporcoes,
            vertical_alignment="center",
        )

        h1.markdown("**Produto**")
        h2.markdown("**Fornecedor**")
        h3.markdown("**Qtd.**")
        h4.markdown("**Valor total**")
        h5.markdown("**Data**")
        h6.markdown("**Ações**")

        separador()

        for indice, compra in enumerate(listaCompras):

            c1, c2, c3, c4, c5, c6 = st.columns(
                proporcoes,
                vertical_alignment="center",
            )

            valorTotal = compra.valor_unit * compra.qtde

            with c1:
                st.markdown(
                    f"**{obter_nome_produto(compra)}**"
                )

            with c2:
                st.write(
                    compra.fornecedor.nome
                    if compra.fornecedor
                    else "Não informado"
                )

            with c3:
                st.write(compra.qtde)

            with c4:
                st.write(formatar_moeda(valorTotal))

            with c5:
                st.write(formatar_data(compra.data_compra))

            with c6:
                visualizar = st.button(
                    ":material/visibility:",
                    key=f"view_compra_{compra.id}",
                    help="Visualizar compra",
                    use_container_width=True,
                )

            if visualizar:
                st.session_state["compra_selecionada"] = compra.id

                st.rerun()

            if indice < len(listaCompras) - 1:
                separador()