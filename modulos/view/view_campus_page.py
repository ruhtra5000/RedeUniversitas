import re
import streamlit as st
from modulos.academico.academico_db import (dbListarCampusCnpj, dbListarCampusId)
from modulos.utils.view_utils import formatar_cnpj

# Função para limpar a consulta de campus
def limpar_consulta_campus():
    st.session_state.pop("consulta_campus_id", None)
    st.session_state.pop("consulta_campus_cnpj", None)
    st.session_state.pop("consulta_campus_id_digitado", None)

# Tela de visualização de campus
def telaViewCampus():

    st.title("🔎 Consulta de Campus")
    st.caption("Pesquise um campus pelo CNPJ ou pelo ID.")

    if "campus_id" in st.session_state:
        st.session_state["consulta_campus_id"] = (
            st.session_state.pop("campus_id")
        )

    campus = None

    col_voltar, _ = st.columns([1, 5])

    with col_voltar:
        if st.button("⬅ Voltar", use_container_width=True):
            from modulos.rotas import listagem_campus_page
            st.switch_page(listagem_campus_page)

    with st.form("buscar_campus", border=True):

        st.markdown("#### 🔍 Buscar campus")

        col1, col2 = st.columns(2)

        with col1:
            cnpjDigitado = st.text_input(
                "CNPJ",
                placeholder="Somente números",
                key="consulta_campus_cnpj",
            )

        with col2:
            idDigitado = st.text_input(
                "ID",
                placeholder="Ex.: 1",
                key="consulta_campus_id_digitado",
            )

        colunaBotao, _ = st.columns([1.3, 4.7])

        with colunaBotao:
            buscar = st.form_submit_button(
                "🔍 Buscar",
                type="primary",
                use_container_width=True,
            )

    if buscar:

        st.session_state.pop("consulta_campus_id", None)

        cnpj = re.sub(r"\D", "", cnpjDigitado)
        idCampus = idDigitado.strip()

        if not cnpj and not idCampus:
            st.warning("Informe um CNPJ ou um ID.")

        elif cnpj and idCampus:
            st.warning(
                "Informe somente o CNPJ ou somente o ID."
            )

        elif cnpj:
            if len(cnpj) != 14:
                st.error("O CNPJ deve possuir 14 números.")
            else:
                campus = dbListarCampusCnpj(cnpj)

                if campus is None:
                    st.error("Campus não encontrado.")
                else:
                    st.session_state["consulta_campus_id"] = (
                        campus.id
                    )

        else:
            if not idCampus.isdigit():
                st.error("O ID deve conter somente números.")
            else:
                campus = dbListarCampusId(int(idCampus))

                if campus is None:
                    st.error("Campus não encontrado.")
                else:
                    st.session_state["consulta_campus_id"] = (
                        campus.id
                    )

    idCampus = st.session_state.get("consulta_campus_id")

    if campus is None and idCampus is not None:
        campus = dbListarCampusId(idCampus)

    if campus is None:
        if not buscar:
            st.info(
                "Informe um CNPJ ou ID para consultar um campus."
            )

        return

    st.write("")

    titulo, botao = st.columns(
        [4.7, 1.3],
        vertical_alignment="center",
    )

    with titulo:
        st.subheader(f"🏛️ {campus.nome}")

    with botao:
        st.button(
            "Limpar",
            icon=":material/close:",
            use_container_width=True,
            on_click=limpar_consulta_campus,
        )

    with st.container(border=True):

        st.markdown("#### 🏛️ Dados do Campus")

        col1, col2, col3 = st.columns([1, 3, 2])

        with col1:
            exibir_campo(
                "ID",
                campus.id,
            )

        with col2:
            exibir_campo(
                "Nome",
                campus.nome,
            )

        with col3:
            exibir_campo(
                "CNPJ",
                formatar_cnpj(campus.cnpj),
            )

        st.write("")

        col1, col2 = st.columns([3.5, 2.5])

        with col1:
            exibir_campo(
                "E-mail",
                campus.email or "Não informado",
            )

        with col2:
            exibir_campo(
                "Telefone",
                campus.telefone or "Não informado",
            )