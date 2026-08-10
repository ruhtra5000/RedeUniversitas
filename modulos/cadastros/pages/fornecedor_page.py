import re
import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from database.entidades.Fornecedor import Fornecedor
from modulos.cadastros.fornecedor import criarFornecedor
from modulos.utils.cadastro_visual import (painelCadastro, renderizarBotaoCadastro, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro)

# Tela de cadastro para Fornecedores
def telaCadastroFornecedor():
    if "form_key_forn" not in st.session_state:
        st.session_state.form_key_forn = 0

    # Função para voltar à página de cadastros
    def voltarCadastros():
        from modulos.rotas import cadastros_page

        st.switch_page(cadastros_page)

    renderizarTopoCadastro(
        titulo="Cadastrar fornecedor",
        descricao=(
            "Registre uma nova empresa fornecedora e seus " "canais de contato."
        ),
        aoVoltar=voltarCadastros,
        prefixoChave="cadastro_fornecedor",
    )

    if st.session_state.pop("cadastro_forn_realizado", False):
        st.toast(
            "Fornecedor cadastrado com sucesso!",
            icon=":material/check:",
        )

    with painelCadastro(
        titulo="Informações do fornecedor",
        descricao=(
            "Preencha a identificação empresarial e os " "dados de comunicação."
        ),
    ):

        renderizarSecaoCadastro(
            numero=1,
            titulo="Dados da empresa",
            descricao="Razão social e identificação fiscal.",
        )

        colNome, colCnpj = st.columns([3, 2])

        with colNome:
            nome = st.text_input(
                "Razão social *",
                placeholder="Ex.: Distribuidora X",
                key=(f"forn_nome_" f"{st.session_state.form_key_forn}"),
            )

        with colCnpj:
            cnpj = st.text_input(
                "CNPJ *",
                placeholder="Somente números",
                key=(f"forn_cnpj_" f"{st.session_state.form_key_forn}"),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Contato",
            descricao="Telefone e endereço eletrônico da empresa.",
        )

        colTelefone, colEmail = st.columns([2, 3])

        with colTelefone:
            telefone = st.text_input(
                "Telefone *",
                placeholder="Ex.: 11999999999",
                key=(f"forn_telefone_" f"{st.session_state.form_key_forn}"),
            )

        with colEmail:
            email = st.text_input(
                "E-mail *",
                placeholder="contato@empresa.com",
                key=(f"forn_email_" f"{st.session_state.form_key_forn}"),
            )

        cadastrar = renderizarBotaoCadastro(
            rotulo="Cadastrar fornecedor",
            icone=":material/business:",
            chave=(f"btn_cad_forn_" f"{st.session_state.form_key_forn}"),
        )

    if cadastrar:
        if (
            not nome.strip()
            or not cnpj.strip()
            or not email.strip()
            or not telefone.strip()
        ):
            st.error("Por favor, preencha todos os campos obrigatórios.")

        else:
            try:
                novo_fornecedor = Fornecedor(
                    cnpj=re.sub(r"\D", "", cnpj),
                    nome=nome.strip(),
                    email=email.strip(),
                    telefone=telefone.strip(),
                )

                criarFornecedor(fornecedor=novo_fornecedor)

                st.session_state.form_key_forn += 1
                st.session_state.pop("cache_fornecedores", None)
                st.session_state["cadastro_forn_realizado"] = True

                st.rerun()

            except SQLAlchemyError as erro:
                st.error("Erro ao salvar os dados no banco: " f"{erro}")

            except Exception as erro:
                st.error(str(erro))
