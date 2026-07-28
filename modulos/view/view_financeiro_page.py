import re
import streamlit as st
from modulos.academico.academico_db import (dbListarFinanceiroCpf, dbListarFinanceiroId)
from modulos.utils.view_utils import (exibirCampo, formatar_cpf)

# Função para limpar a consulta de financeiro
def limparConsultaFinanceiro():
    st.session_state.pop("consulta_financeiro_id", None)
    st.session_state.pop("consulta_financeiro_cpf", None)
    st.session_state.pop("consulta_financeiro_id_digitado", None)

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
            from modulos.rotas import listagem_financeiro_page
            st.switch_page(listagem_financeiro_page)

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
                financeiro = dbListarFinanceiroCpf(cpf)

                if financeiro is None:
                    st.error("Funcionário não encontrado.")
                else:
                    st.session_state["consulta_financeiro_id"] = (
                        financeiro.pessoa_id
                    )

        elif not idPessoa.isdigit():
            st.error("O ID deve conter somente números.")

        else:
            financeiro = dbListarFinanceiroId(int(idPessoa))

            if financeiro is None:
                st.error("Funcionário não encontrado.")
            else:
                st.session_state["consulta_financeiro_id"] = (
                    financeiro.pessoa_id
                )

    idPessoa = st.session_state.get("consulta_financeiro_id")

    if financeiro is None and idPessoa is not None:
        financeiro = dbListarFinanceiroId(idPessoa)

    if financeiro is None:
        if not buscar:
            st.info("Informe um CPF ou ID para consultar.")

        return

    st.write("")

    titulo, botao = st.columns(
        [4.7, 1.3],
        vertical_alignment="center",
    )

    with titulo:
        st.subheader(f"💰 {financeiro.pessoa.nome}")

    with botao:
        st.button(
            "Limpar",
            icon=":material/close:",
            use_container_width=True,
            on_click=limparConsultaFinanceiro,
        )

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