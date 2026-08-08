import streamlit as st
from modulos.estoque.estoque_service import listarAlmoxarifes
from modulos.utils.listagem_utils import formatar_cpf, separador

# Tela de listagem para Almoxarifes
def telaListagemAlmoxarifes():

    st.title("📋 Listagem de Almoxarifes")
    st.caption("Consulte os almoxarifes cadastrados no sistema.")

    colVoltar, _ = st.columns([1, 5])

    with colVoltar:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import home_page
            st.switch_page(home_page)

    listaAlmoxarifes = listarAlmoxarifes()

    if not listaAlmoxarifes:
        st.info("📦 Nenhum almoxarife cadastrado.")
        return

    st.write("")

    st.caption(
        f"📦 {len(listaAlmoxarifes)} "
        f"{'almoxarife encontrado' if len(listaAlmoxarifes) == 1 else 'almoxarifes encontrados'}"
    )

    proporcoes = [3, 2.2, 3.2, 2.5, 1.3]

    with st.container(border=True):

        h1, h2, h3, h4, h5 = st.columns(
            proporcoes,
            vertical_alignment="center",
        )

        h1.markdown("**Almoxarife**")
        h2.markdown("**CPF**")
        h3.markdown("**E-mail**")
        h4.markdown("**Campus**")
        h5.markdown("**Ações**")

        separador()

        for indice, almoxarife in enumerate(listaAlmoxarifes):

            c1, c2, c3, c4, c5 = st.columns(
                proporcoes,
                vertical_alignment="center",
            )

            with c1:
                st.markdown(f"**{almoxarife.pessoa.nome}**")

            with c2:
                st.write(formatar_cpf(almoxarife.pessoa.cpf))

            with c3:
                st.write(
                    almoxarife.pessoa.email or "Não informado"
                )

            with c4:
                st.write(
                    almoxarife.campus.nome
                    if almoxarife.campus
                    else "Não informado"
                )

            with c5:
                visualizar = st.button(
                    "👁️",
                    key=f"view_almoxarife_{almoxarife.pessoa_id}",
                    help="Visualizar almoxarife",
                    use_container_width=True,
                )

            if visualizar:
                st.session_state["almoxarife_id"] = (
                    almoxarife.pessoa_id
                )

                st.rerun()

            if indice < len(listaAlmoxarifes) - 1:
                separador()