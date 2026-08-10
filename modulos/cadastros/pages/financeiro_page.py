import re
import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from database.entidades.Pessoa import Pessoa
from modulos.academico.academico_service import listarCampus
from modulos.cadastros.financeiro import criarFinanceiro
from modulos.utils.cadastro_visual import (painelCadastro, renderizarAvisoCadastro, renderizarBotaoCadastro, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro)

# Tela de cadastro para Funcionários Financeiros
def telaCadastroFinanceiro():
    if "form_key_fin" not in st.session_state:
        st.session_state.form_key_fin = 0

    # Função para voltar à página de cadastros
    def voltarCadastros():
        from modulos.rotas import cadastros_page

        st.switch_page(cadastros_page)

    renderizarTopoCadastro(
        titulo="Cadastrar financeiro",
        descricao=(
            "Inclua um funcionário da área financeira e defina "
            "seu campus de atuação."
        ),
        aoVoltar=voltarCadastros,
        prefixoChave="cadastro_financeiro",
    )

    if st.session_state.pop("cadastro_fin_realizado", False):
        st.toast(
            "Funcionário financeiro cadastrado com sucesso!",
            icon=":material/check:",
        )

    if "cache_campus" not in st.session_state:
        st.session_state.cache_campus = listarCampus()

    lista_campus = st.session_state.cache_campus

    if not lista_campus:
        renderizarAvisoCadastro(
            titulo="Campus necessário",
            descricao=(
                "Cadastre pelo menos um campus antes de adicionar "
                "um funcionário financeiro."
            ),
        )

    with painelCadastro(
        titulo="Informações do funcionário",
        descricao=(
            "Preencha os dados pessoais e o vínculo " "institucional do profissional."
        ),
    ):

        renderizarSecaoCadastro(
            numero=1,
            titulo="Dados pessoais",
            descricao="Informações de identificação e contato.",
        )

        colNome, colEmail = st.columns(2)

        with colNome:
            nome = st.text_input(
                "Nome completo *",
                placeholder="Ex.: Carlos Mendes",
                key=(f"fin_nome_" f"{st.session_state.form_key_fin}"),
            )

        with colEmail:
            email = st.text_input(
                "E-mail *",
                placeholder="email@exemplo.com",
                key=(f"fin_email_" f"{st.session_state.form_key_fin}"),
            )

        colCpf, colTelefone = st.columns(2)

        with colCpf:
            cpf = st.text_input(
                "CPF *",
                placeholder="Somente números",
                key=(f"fin_cpf_" f"{st.session_state.form_key_fin}"),
            )

        with colTelefone:
            telefone = st.text_input(
                "Telefone",
                placeholder="Opcional",
                key=(f"fin_telefone_" f"{st.session_state.form_key_fin}"),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Vínculo institucional",
            descricao="Campus em que o funcionário atuará.",
        )

        campus = st.selectbox(
            "Campus *",
            options=lista_campus if lista_campus else [],
            format_func=lambda item: item.nome,
            index=None,
            placeholder="Selecione um campus...",
            disabled=not lista_campus,
            key=(f"fin_campus_" f"{st.session_state.form_key_fin}"),
        )

        cadastrar = renderizarBotaoCadastro(
            rotulo="Cadastrar financeiro",
            icone=":material/person_add:",
            chave=(f"btn_cad_fin_" f"{st.session_state.form_key_fin}"),
        )

    if cadastrar:
        if not lista_campus:
            st.error("Cadastre pelo menos um Campus antes de continuar.")

        elif not nome.strip() or not cpf.strip() or not email.strip():
            st.error("Por favor, preencha todos os campos obrigatórios.")

        elif campus is None:
            st.error("Por favor, selecione um Campus.")

        else:
            try:
                nova_pessoa = Pessoa(
                    nome=nome.strip(),
                    cpf=re.sub(r"\D", "", cpf),
                    email=email.strip(),
                    telefone=(telefone.strip() if telefone.strip() else None),
                )

                criarFinanceiro(
                    pessoa=nova_pessoa,
                    idCampus=campus.id,
                )

                st.session_state.form_key_fin += 1
                st.session_state["cadastro_fin_realizado"] = True

                st.rerun()

            except SQLAlchemyError as erro:
                st.error("Erro ao salvar os dados no banco: " f"{erro}")

            except Exception as erro:
                st.error(str(erro))
