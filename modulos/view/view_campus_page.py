import re
import streamlit as st
from modulos.academico.academico_service import listarCampusCnpj, listarCampusId
from modulos.utils.view_utils import formatar_cnpj, exibirCampo, limpar_consulta_campus

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
            pass

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
                campus = listarCampusCnpj(cnpj)

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
                campus = listarCampusId(int(idCampus))

                if campus is None:
                    st.error("Campus não encontrado.")
                else:
                    st.session_state["consulta_campus_id"] = (
                        campus.id
                    )

    idCampus = st.session_state.get("consulta_campus_id")

    if campus is None and idCampus is not None:
        campus = listarCampusId(idCampus)

    if campus is None:
        if not buscar:
            st.info(
                "Informe um CNPJ ou ID para consultar um campus."
            )

        return

    st.write("")

    titulo, botao_limpar, botao_editar = st.columns(
        [4.2, 0.9, 0.9],
        vertical_alignment="center",
    )

    with titulo:
        st.subheader(f"🏛️ {campus.nome}")

    with botao_limpar:
        st.button(
            "Limpar",
            icon=":material/close:",
            use_container_width=True,
            on_click=limpar_consulta_campus,
        )

    with botao_editar:
        if "ADMIN" in st.session_state.roles:
            if st.button(
                "Editar",
                icon=":material/edit:",
                use_container_width=True,
                type="secondary"
            ):
                st.session_state["edicao_campus_id"] = campus.id
                from modulos.rotas import editar_campus_page
                st.switch_page(editar_campus_page)

    with st.container(border=True):

        st.markdown("#### 🏛️ Dados do Campus")

        col1, col2, col3 = st.columns([1, 3, 2])

        with col1:
            exibirCampo(
                "ID",
                campus.id,
            )

        with col2:
            exibirCampo(
                "Nome",
                campus.nome,
            )

        with col3:
            exibirCampo(
                "CNPJ",
                formatar_cnpj(campus.cnpj),
            )

        st.write("")

        col1, col2 = st.columns([3.5, 2.5])

        with col1:
            exibirCampo(
                "E-mail",
                campus.email or "Não informado",
            )

        with col2:
            exibirCampo(
                "Telefone",
                campus.telefone or "Não informado",
            )