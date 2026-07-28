import re
import streamlit as st
from modulos.academico.academico_db import dbListarCampus
from modulos.utils.listagem_utils import separador
from modulos.utils.view_utils import exibirCampo

# Função para formatar o CNPJ
def formatar_cnpj(cnpj):
    numeros = re.sub(r"\D", "", cnpj or "")

    if len(numeros) != 14:
        return cnpj or "Não informado"

    return (
        f"{numeros[:2]}.{numeros[2:5]}."
        f"{numeros[5:8]}/{numeros[8:12]}-"
        f"{numeros[12:]}"
    )

# Tela de listagem para Campus
def telaListagemCampus():

    st.title("📋 Listagem de Campus")
    st.caption("Consulte os campus cadastrados no sistema.")

    colVoltar, _ = st.columns([1, 5])

    with colVoltar:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import home_page
            st.switch_page(home_page)

    listaCampus = dbListarCampus()

    if not listaCampus:
        st.info("🏛️ Nenhum campus cadastrado.")
        return

    st.write("")

    st.caption(
        f"🏛️ {len(listaCampus)} "
        f"{'campus encontrado' if len(listaCampus) == 1 else 'campus encontrados'}"
    )

    proporcoes = [3, 2.2, 3.2, 2.5, 1.3]

    with st.container(border=True):

        h1, h2, h3, h4, h5 = st.columns(
            proporcoes,
            vertical_alignment="center",
        )

        h1.markdown("**Campus**")
        h2.markdown("**CNPJ**")
        h3.markdown("**E-mail**")
        h4.markdown("**Telefone**")
        h5.markdown("**Ações**")

        separador()

        for indice, campus in enumerate(listaCampus):

            c1, c2, c3, c4, c5 = st.columns(
                proporcoes,
                vertical_alignment="center",
            )

            with c1:
                st.markdown(f"**{campus.nome}**")

            with c2:
                st.write(formatar_cnpj(campus.cnpj))

            with c3:
                st.write(campus.email or "Não informado")

            with c4:
                st.write(campus.telefone or "Não informado")

            with c5:
                visualizar = st.button(
                    "👁️",
                    key=f"view_campus_{campus.id}",
                    help="Visualizar campus",
                    use_container_width=True,
                )

            if visualizar:
                st.session_state["campus_id"] = campus.id

                from modulos.rotas import view_campus_page
                st.switch_page(view_campus_page)

            if indice < len(listaCampus) - 1:
                separador()