import re
import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from database.entidades.Pessoa import Pessoa
from modulos.academico.academico_service import listarCampus
from modulos.cadastros.almoxarife import criarAlmoxarife
from modulos.utils.cadastro_visual import (painelCadastro, renderizarAvisoCadastro, renderizarBotaoCadastro, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro)

# Tela de cadastro para Almoxarifes
def telaCadastroAlmoxarife():
    if "form_key_alm" not in st.session_state:
        st.session_state.form_key_alm = 0

    # Função para voltar à página de cadastros
    def voltarCadastros():
        from modulos.rotas import cadastros_page

        st.switch_page(cadastros_page)

    renderizarTopoCadastro(
        titulo="Cadastrar almoxarife",
        descricao=(
            "Inclua um novo profissional e defina o campus " "ao qual ficará vinculado."
        ),
        aoVoltar=voltarCadastros,
        prefixoChave="cadastro_almoxarife",
    )

    if st.session_state.pop("cadastro_alm_realizado", False):
        st.toast(
            "Almoxarife cadastrado com sucesso!",
            icon=":material/check:",
        )

    if "cache_campus" not in st.session_state:
        st.session_state.cache_campus = listarCampus()

    listaCampus = st.session_state.cache_campus

    if not listaCampus:
        renderizarAvisoCadastro(
            titulo="Campus necessário",
            descricao=(
                "Cadastre pelo menos um campus antes de adicionar " "um almoxarife."
            ),
        )

    with painelCadastro(
        titulo="Informações do almoxarife",
        descricao=(
            "Preencha os dados pessoais e o vínculo " "institucional do profissional."
        ),
    ):

        renderizarSecaoCadastro(
            numero=1,
            titulo="Dados pessoais",
            descricao=("Informações de identificação e contato " "do profissional."),
        )

        colNome, colEmail = st.columns(2)

        with colNome:
            nome = st.text_input(
                "Nome completo *",
                placeholder="Ex.: Maria Oliveira",
                key=(f"alm_nome_" f"{st.session_state.form_key_alm}"),
            )

        with colEmail:
            email = st.text_input(
                "E-mail *",
                placeholder="email@exemplo.com",
                key=(f"alm_email_" f"{st.session_state.form_key_alm}"),
            )

        colCpf, colTelefone = st.columns(2)

        with colCpf:
            cpf = st.text_input(
                "CPF *",
                placeholder="Somente números",
                key=(f"alm_cpf_" f"{st.session_state.form_key_alm}"),
            )

        with colTelefone:
            telefone = st.text_input(
                "Telefone",
                placeholder="Opcional",
                key=(f"alm_telefone_" f"{st.session_state.form_key_alm}"),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Vínculo institucional",
            descricao=("Selecione a unidade em que o profissional " "atuará."),
        )

        campus = st.selectbox(
            "Campus *",
            options=listaCampus if listaCampus else [],
            format_func=lambda item: item.nome,
            index=None,
            placeholder="Selecione um campus...",
            disabled=not listaCampus,
            key=(f"alm_campus_" f"{st.session_state.form_key_alm}"),
        )

        cadastrar = renderizarBotaoCadastro(
            rotulo="Cadastrar almoxarife",
            icone=":material/person_add:",
            chave=(f"btn_cad_alm_" f"{st.session_state.form_key_alm}"),
        )

    if cadastrar:
        if not listaCampus:
            st.error("Cadastre pelo menos um Campus antes de continuar.")

        elif not nome.strip() or not cpf.strip() or not email.strip():
            st.error("Por favor, preencha todos os campos obrigatórios.")

        elif campus is None:
            st.error("Por favor, selecione um Campus.")

        else:
            try:
                novaPessoa = Pessoa(
                    nome=nome.strip(),
                    cpf=re.sub(r"\D", "", cpf),
                    email=email.strip(),
                    telefone=(telefone.strip() if telefone.strip() else None),
                )

                criarAlmoxarife(
                    pessoa=novaPessoa,
                    idCampus=campus.id,
                )

                st.session_state.form_key_alm += 1
                st.session_state["cadastro_alm_realizado"] = True

                st.rerun()

            except SQLAlchemyError as erro:
                st.error("Erro ao salvar os dados no banco: " f"{erro}")

            except Exception as erro:
                st.error(str(erro))
