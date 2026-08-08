import re
import streamlit as st
from modulos.estoque.estoque_service import listarAlmoxarifeCpf, listarAlmoxarifeId
from modulos.utils.view_utils import exibirCampo, formatar_cpf, limpar_consulta_almoxarife

# Tela de visualização de almoxarife
def telaViewAlmoxarife():

    st.title("🔎 Consulta de Almoxarife")
    st.caption("Pesquise um almoxarife pelo CPF ou pelo ID.")

    if "almoxarife_id" in st.session_state:
        st.session_state["consulta_almoxarife_id"] = (
            st.session_state.pop("almoxarife_id")
        )

    almoxarife = None

    colVoltar, _ = st.columns([1, 5])

    with colVoltar:
        if st.button("⬅ Voltar", use_container_width=True):
            pass

    with st.form("buscar_almoxarife", border=True):

        st.markdown("#### 🔍 Buscar almoxarife")

        col1, col2 = st.columns(2)

        with col1:
            cpfDigitado = st.text_input(
                "CPF",
                placeholder="Somente números",
                key="consulta_almoxarife_cpf",
            )

        with col2:
            idDigitado = st.text_input(
                "ID",
                placeholder="Ex.: 1",
                key="consulta_almoxarife_id_digitado",
            )

        colunaBotao, _ = st.columns([1.3, 4.7])

        with colunaBotao:
            buscar = st.form_submit_button(
                "🔍 Buscar",
                type="primary",
                use_container_width=True,
            )

    if buscar:
        st.session_state.pop("consulta_almoxarife_id", None)

        cpf = re.sub(r"\D", "", cpfDigitado)
        idPessoa = idDigitado.strip()

        if not cpf and not idPessoa:
            st.warning("Informe um CPF ou um ID.")

        elif cpf and idPessoa:
            st.warning("Informe somente o CPF ou somente o ID.")

        elif cpf:
            if len(cpf) != 11:
                st.error("O CPF deve possuir 11 números.")
            else:
                almoxarife = listarAlmoxarifeCpf(cpf)

                if almoxarife is None:
                    st.error("Almoxarife não encontrado.")
                else:
                    st.session_state["consulta_almoxarife_id"] = (
                        almoxarife.pessoa_id
                    )

        elif not idPessoa.isdigit():
            st.error("O ID deve conter somente números.")

        else:
            almoxarife = listarAlmoxarifeId(int(idPessoa))

            if almoxarife is None:
                st.error("Almoxarife não encontrado.")
            else:
                st.session_state["consulta_almoxarife_id"] = (
                    almoxarife.pessoa_id
                )

    idPessoa = st.session_state.get("consulta_almoxarife_id")

    if almoxarife is None and idPessoa is not None:
        almoxarife = listarAlmoxarifeId(idPessoa)

    if almoxarife is None:
        if not buscar:
            st.info("Informe um CPF ou ID para consultar.")

        return

    st.write("")

    titulo, botao_limpar, botao_editar = st.columns(
        [4.2, 0.9, 0.9],
        vertical_alignment="center",
    )

    with titulo:
        st.subheader(f"📦 {almoxarife.pessoa.nome}")

    with botao_limpar:
        st.button(
            "Limpar",
            icon=":material/close:",
            use_container_width=True,
            on_click=limpar_consulta_almoxarife,
        )

    with botao_editar:
        if "ADMIN" in st.session_state.roles:
            if st.button(
                "Editar",
                icon=":material/edit:",
                use_container_width=True,
                type="secondary"
            ):
                st.session_state["edicao_almoxarife_id"] = almoxarife.pessoa_id
                from modulos.rotas import editar_almoxarife_page
                st.switch_page(editar_almoxarife_page)

    with st.container(border=True):

        st.markdown("#### 👤 Dados Pessoais")

        col1, col2, col3 = st.columns([1, 3, 2])

        with col1:
            exibirCampo("ID", almoxarife.pessoa_id)

        with col2:
            exibirCampo("Nome", almoxarife.pessoa.nome)

        with col3:
            exibirCampo(
                "CPF",
                formatar_cpf(almoxarife.pessoa.cpf),
            )

        st.write("")

        col1, col2 = st.columns([3.5, 2.5])

        with col1:
            exibirCampo("E-mail", almoxarife.pessoa.email)

        with col2:
            exibirCampo("Telefone", almoxarife.pessoa.telefone)

    st.write("")

    with st.container(border=True):
        st.markdown("#### 🏛️ Vínculo")

        exibirCampo(
            "Campus",
            almoxarife.campus.nome
            if almoxarife.campus
            else "Não informado",
        )