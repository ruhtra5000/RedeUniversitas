import re
from decimal import Decimal
import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from database.entidades.Caixa import Caixa
from database.entidades.Campus import Campus
from modulos.cadastros.campus import criarCampus
from modulos.utils.cadastro_visual import (painelCadastro, renderizarBotaoCadastro, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro)

# Tela de cadastro para Campus
def telaCadastroCampus():
    if "form_key_campus" not in st.session_state:
        st.session_state.form_key_campus = 0

    # Função para voltar à página de cadastros
    def voltarCadastros():
        from modulos.rotas import cadastros_page

        st.switch_page(cadastros_page)

    renderizarTopoCadastro(
        titulo="Cadastrar campus",
        descricao=(
            "Registre uma nova unidade institucional e seus " "dados de contato."
        ),
        aoVoltar=voltarCadastros,
        prefixoChave="cadastro_campus",
    )

    if st.session_state.pop("cadastro_campus_realizado", False):
        st.toast(
            "Campus cadastrado com sucesso!",
            icon=":material/check:",
        )

    with painelCadastro(
        titulo="Informações do campus",
        descricao=(
            "Preencha os dados da unidade, sua localização " "e os canais de contato."
        ),
    ):

        renderizarSecaoCadastro(
            numero=1,
            titulo="Dados da unidade",
            descricao="Identificação institucional e caixa inicial.",
        )

        colNome, colCnpj, colCaixa = st.columns([2, 1.5, 1.3])

        with colNome:
            nome = st.text_input(
                "Nome do campus *",
                placeholder="Ex.: Campus Central",
                key=(f"campus_nome_" f"{st.session_state.form_key_campus}"),
            )

        with colCnpj:
            cnpj = st.text_input(
                "CNPJ *",
                placeholder="Somente números",
                key=(f"campus_cnpj_" f"{st.session_state.form_key_campus}"),
            )

        with colCaixa:
            valor_caixa = st.number_input(
                "Valor inicial do caixa (R$)",
                min_value=0.0,
                step=100.0,
                format="%.2f",
                key=(f"campus_caixa_" f"{st.session_state.form_key_campus}"),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Localização",
            descricao="Cidade e unidade federativa do campus.",
        )

        colCidade, colEstado = st.columns([4, 1])

        with colCidade:
            cidade = st.text_input(
                "Cidade *",
                placeholder="Ex.: São Paulo",
                key=(f"campus_cidade_" f"{st.session_state.form_key_campus}"),
            )

        with colEstado:
            estado = st.text_input(
                "Estado *",
                placeholder="Ex.: SP",
                max_chars=2,
                key=(f"campus_estado_" f"{st.session_state.form_key_campus}"),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=3,
            titulo="Contato",
            descricao="Canais oficiais de comunicação da unidade.",
        )

        colEmail, colTelefone = st.columns([3, 2])

        with colEmail:
            email = st.text_input(
                "E-mail *",
                placeholder="contato@campus.com",
                key=(f"campus_email_" f"{st.session_state.form_key_campus}"),
            )

        with colTelefone:
            telefone = st.text_input(
                "Telefone",
                placeholder="Opcional",
                key=(f"campus_telefone_" f"{st.session_state.form_key_campus}"),
            )

        cadastrar = renderizarBotaoCadastro(
            rotulo="Cadastrar campus",
            icone=":material/domain_add:",
            chave=(f"btn_cad_campus_" f"{st.session_state.form_key_campus}"),
        )

    if cadastrar:
        if not nome.strip() or not cnpj.strip() or not email.strip():
            st.error(
                "Por favor, preencha todos os campos obrigatórios "
                "(Nome, CNPJ e E-mail)."
            )

        else:
            try:
                novo_campus = Campus(
                    cnpj=re.sub(r"\D", "", cnpj),
                    nome=nome.strip(),
                    email=email.strip(),
                    telefone=(telefone.strip() if telefone.strip() else None),
                )

                criarCampus(
                    campus=novo_campus,
                    valorInicialCaixa=valor_caixa,
                )

                st.session_state.form_key_campus += 1
                st.session_state.pop("cache_campus", None)
                st.session_state["cadastro_campus_realizado"] = True

                st.rerun()

            except SQLAlchemyError as erro:
                st.error("Erro ao salvar os dados no banco: " f"{erro}")

            except Exception as erro:
                st.error(str(erro))
