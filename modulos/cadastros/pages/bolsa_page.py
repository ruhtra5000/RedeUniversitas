import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from database.entidades.Bolsa import Bolsa
from database.entidades.enums.StatusBolsa import StatusBolsa
from modulos.academico.academico_service import listarAlunos, listarAlunosAtivos
from modulos.cadastros.bolsa import criarBolsa
from modulos.utils.cadastro_visual import (painelCadastro, renderizarAvisoCadastro, renderizarBotaoCadastro, renderizarDivisorCadastro, renderizarSecaoCadastro, renderizarTopoCadastro)

# Tela de cadastro para Bolsas
def telaCadastroBolsa():
    if "form_key_bolsa" not in st.session_state:
        st.session_state.form_key_bolsa = 0

    # Função para voltar à página de cadastros
    def voltarCadastros():
        from modulos.rotas import cadastros_page

        st.switch_page(cadastros_page)

    # Função para abrir a página de edições de bolsas
    def abrirEdicoes():
        from modulos.rotas import gestao_bolsas

        st.switch_page(gestao_bolsas)

    renderizarTopoCadastro(
        titulo="Cadastrar bolsa",
        descricao=(
            "Conceda um benefício acadêmico e defina suas " "condições de vigência."
        ),
        aoVoltar=voltarCadastros,
        prefixoChave="cadastro_bolsa",
        rotuloAcao="Edições",
        iconeAcao=":material/edit:",
        aoAcao=abrirEdicoes,
    )

    if st.session_state.pop("cadastro_bolsa_realizado", False):
        st.toast(
            "Bolsa cadastrada com sucesso!",
            icon=":material/check:",
        )

    if "cache_alunos" not in st.session_state:
        st.session_state.cache_alunos = listarAlunos()

    lista_alunos = listarAlunosAtivos()

    if not lista_alunos:
        renderizarAvisoCadastro(
        titulo="Aluno ativo necessário",
        descricao=("É necessário possuir pelo menos um aluno ativo para conceder uma bolsa.")
    )

    with painelCadastro(
        titulo="Informações da bolsa",
        descricao=(
            "Selecione o beneficiário e configure o desconto, " "status e período."
        ),
    ):

        renderizarSecaoCadastro(
            numero=1,
            titulo="Beneficiário",
            descricao="Aluno contemplado e modalidade do benefício.",
        )

        colAluno, colTipo = st.columns(2)

        with colAluno:
            aluno_selecionado = st.selectbox(
                "Aluno *",
                options=lista_alunos if lista_alunos else [],
                format_func=lambda aluno: aluno.pessoa.nome,
                index=None,
                placeholder="Selecione um aluno...",
                disabled=not lista_alunos,
                key=(f"bolsa_aluno_" f"{st.session_state.form_key_bolsa}"),
            )

        with colTipo:
            tipo_bolsa = st.text_input(
                "Tipo de bolsa *",
                placeholder="Ex.: Bolsa Mérito, Bolsa Atleta",
                key=(f"bolsa_tipo_" f"{st.session_state.form_key_bolsa}"),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=2,
            titulo="Condições",
            descricao="Percentual concedido e situação atual da bolsa.",
        )

        colPercentual, colStatus = st.columns(2)

        with colPercentual:
            percentual_desconto = st.number_input(
                "Percentual de desconto (%) *",
                min_value=1,
                max_value=100,
                step=1,
                format="%d",
                help="Digite um valor de 1 a 100.",
                key=(f"bolsa_perc_" f"{st.session_state.form_key_bolsa}"),
            )

        with colStatus:
            status_bolsa = st.selectbox(
                "Status da bolsa *",
                options=list(StatusBolsa),
                format_func=lambda status: status.name.title(),
                key=(f"bolsa_status_" f"{st.session_state.form_key_bolsa}"),
            )

        renderizarDivisorCadastro()

        renderizarSecaoCadastro(
            numero=3,
            titulo="Vigência",
            descricao="Período em que o benefício permanecerá válido.",
        )

        colInicio, colFim = st.columns(2)

        with colInicio:
            data_inicio = st.date_input(
                "Data de início *",
                format="DD/MM/YYYY",
                key=(f"bolsa_inicio_" f"{st.session_state.form_key_bolsa}"),
            )

        with colFim:
            data_fim = st.date_input(
                "Data de término *",
                format="DD/MM/YYYY",
                key=(f"bolsa_fim_" f"{st.session_state.form_key_bolsa}"),
            )

        cadastrar = renderizarBotaoCadastro(
            rotulo="Cadastrar bolsa",
            icone=":material/account_balance:",
            chave=(f"btn_cad_bolsa_" f"{st.session_state.form_key_bolsa}"),
        )

    if cadastrar:
        if not lista_alunos:
            st.error("Cadastre pelo menos um Aluno antes de continuar.")

        elif aluno_selecionado is None:
            st.error("Por favor, selecione um Aluno.")

        elif not tipo_bolsa.strip():
            st.error("Por favor, preencha o Tipo de Bolsa.")

        else:
            try:
                nova_bolsa = Bolsa(
                    aluno_id=aluno_selecionado.pessoa_id,
                    tipo_bolsa=tipo_bolsa.strip(),
                    percentual_desconto=(float(percentual_desconto) / 100.0),
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    status=status_bolsa,
                )

                criarBolsa(
                    bolsa=nova_bolsa,
                    aluno=aluno_selecionado,
                )

                st.session_state.form_key_bolsa += 1
                st.session_state["cadastro_bolsa_realizado"] = True

                st.rerun()

            except SQLAlchemyError as erro:
                st.error("Erro ao salvar os dados no banco: " f"{erro}")

            except Exception as erro:
                st.error(str(erro))
