import re
import streamlit as st
from modulos.financeiro.financeiro_service import listarFinanceiroCpf, listarFinanceiroId
from modulos.utils.view_utils import exibirCampo, formatar_cpf, limpar_consulta_financeiro

# Tela de visualização de financeiro
def telaViewFinanceiro():

    st.title("🔎 Consulta do Financeiro")
    st.caption("Pesquise um funcionário pelo CPF ou pelo ID.")

    if "financeiro_id" in st.session_state:
        st.session_state["consulta_financeiro_id"] = (
            st.session_state.pop("financeiro_id")
        )

    financeiro = None

    colVoltar, _ = st.columns([1, 5])

    with colVoltar:
        if st.button("⬅ Voltar", use_container_width=True):
            pass

    with st.form("buscar_financeiro", border=True):

        st.markdown("#### 🔍 Buscar funcionário")

        col1, col2 = st.columns(2)

        with col1:
            cpfDigitado = st.text_input(
                "CPF",
                placeholder="Somente números",
                key="consulta_financeiro_cpf",
            )

        with col2:
            idDigitado = st.text_input(
                "ID",
                placeholder="Ex.: 1",
                key="consulta_financeiro_id_digitado",
            )

        colunaBotao, _ = st.columns([1.3, 4.7])

        with colunaBotao:
            buscar = st.form_submit_button(
                "🔍 Buscar",
                type="primary",
                use_container_width=True,
            )

    if buscar:
        st.session_state.pop("consulta_financeiro_id", None)

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
                financeiro = listarFinanceiroCpf(cpf)

                if financeiro is None:
                    st.error("Funcionário não encontrado.")
                else:
                    st.session_state["consulta_financeiro_id"] = (
                        financeiro.pessoa_id
                    )

        elif not idPessoa.isdigit():
            st.error("O ID deve conter somente números.")

        else:
            financeiro = listarFinanceiroId(int(idPessoa))

            if financeiro is None:
                st.error("Funcionário não encontrado.")
            else:
                st.session_state["consulta_financeiro_id"] = (
                    financeiro.pessoa_id
                )

    idPessoa = st.session_state.get("consulta_financeiro_id")

    if financeiro is None and idPessoa is not None:
        financeiro = listarFinanceiroId(idPessoa)

    if financeiro is None:
        if not buscar:
            st.info("Informe um CPF ou ID para consultar.")

        return

    st.write("")

    titulo, botao_limpar, botao_editar = st.columns(
        [4.2, 0.9, 0.9],
        vertical_alignment="center",
    )

    with titulo:
        st.subheader(f"💰 {financeiro.pessoa.nome}")

    with botao_limpar:
        st.button(
            "Limpar",
            icon=":material/close:",
            use_container_width=True,
            on_click=limpar_consulta_financeiro,
        )

    with botao_editar:
        if "ADMIN" in st.session_state.roles:
            if st.button(
                "Editar",
                icon=":material/edit:",
                use_container_width=True,
                type="secondary"
            ):
                st.session_state["edicao_financeiro_id"] = financeiro.pessoa_id
                from modulos.rotas import editar_financeiro_page
                st.switch_page(editar_financeiro_page)

    with st.container(border=True):

        st.markdown("#### 👤 Dados Pessoais")

        col1, col2, col3 = st.columns([1, 3, 2])

        with col1:
            exibirCampo("ID", financeiro.pessoa_id)

        with col2:
            exibirCampo("Nome", financeiro.pessoa.nome)

        with col3:
            exibirCampo(
                "CPF",
                formatar_cpf(financeiro.pessoa.cpf),
            )

        st.write("")

        col1, col2 = st.columns([3.5, 2.5])

        with col1:
            exibirCampo("E-mail", financeiro.pessoa.email)

        with col2:
            exibirCampo("Telefone", financeiro.pessoa.telefone)

    st.write("")

    with st.container(border=True):
        st.markdown("#### 🏛️ Vínculo")

        exibirCampo(
            "Campus",
            financeiro.campus.nome
            if financeiro.campus
            else "Não informado",
        )