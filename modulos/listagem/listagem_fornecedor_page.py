import re
import streamlit as st
from modulos.compras.compras_service import listarFornecedores
from modulos.utils.listagem_utils import separador, formatar_cnpj

# Tela de listagem para Fornecedores
def telaListagemFornecedores():

    st.title(":material/assignment: Listagem de Fornecedores")
    st.caption(
        "Consulte os fornecedores cadastrados no sistema."
    )

    colVoltar, _ = st.columns([1, 5])

    with colVoltar:
        if st.button(":material/arrow_back: Voltar", use_container_width=True):
            from modulos.rotas import home_page
            st.switch_page(home_page)

    listaFornecedores = listarFornecedores()

    if not listaFornecedores:
        st.info(":material/factory: Nenhum fornecedor cadastrado.")
        return

    st.write("")

    st.caption(
        f":material/factory: {len(listaFornecedores)} "
        f"{'fornecedor encontrado' if len(listaFornecedores) == 1 else 'fornecedores encontrados'}"
    )

    proporcoes = [3, 2.4, 3.2, 2.2, 1.2]

    with st.container(border=True):

        h1, h2, h3, h4, h5 = st.columns(
            proporcoes,
            vertical_alignment="center",
        )

        h1.markdown("**Fornecedor**")
        h2.markdown("**CNPJ**")
        h3.markdown("**E-mail**")
        h4.markdown("**Telefone**")
        h5.markdown("**Ações**")

        separador()

        for indice, fornecedor in enumerate(listaFornecedores):

            c1, c2, c3, c4, c5 = st.columns(
                proporcoes,
                vertical_alignment="center",
            )

            with c1:
                st.markdown(f"**{fornecedor.nome}**")

            with c2:
                st.write(formatar_cnpj(fornecedor.cnpj))

            with c3:
                st.write(
                    fornecedor.email or "Não informado"
                )

            with c4:
                st.write(
                    fornecedor.telefone or "Não informado"
                )

            with c5:
                visualizar = st.button(
                    ":material/visibility:",
                    key=f"view_fornecedor_{fornecedor.id}",
                    help="Visualizar fornecedor",
                    use_container_width=True,
                )

            if visualizar:
                st.session_state["fornecedor_selecionado"] = (
                    fornecedor.id
                )

                st.rerun()

            if indice < len(listaFornecedores) - 1:
                separador()