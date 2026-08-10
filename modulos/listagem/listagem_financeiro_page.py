import streamlit as st
from modulos.financeiro.financeiro_service import listarFinanceiro
from modulos.utils.listagem_utils import formatar_cpf
from modulos.utils.listagem_visual import ColunaListagem, renderizarListagem

# Tela de listagem para Financeiros
def telaListagemFinanceiros():

    listaFinanceiros = listarFinanceiro()

    colunas = [
        ColunaListagem(
            titulo="Funcionário",
            valor=lambda financeiro: (financeiro.pessoa.nome),
            subtitulo="Financeiro",
            proporcao=2.6,
            tipo="principal",
        ),
        ColunaListagem(
            titulo="CPF",
            valor=lambda financeiro: formatar_cpf(financeiro.pessoa.cpf),
            proporcao=1.7,
        ),
        ColunaListagem(
            titulo="E-mail",
            valor=lambda financeiro: (financeiro.pessoa.email or "Não informado"),
            proporcao=2.5,
        ),
        ColunaListagem(
            titulo="Campus",
            valor=lambda financeiro: (
                financeiro.campus.nome if financeiro.campus else "Não informado"
            ),
            proporcao=2.7,
            tipo="badge",
        ),
    ]

    # Função de navegação
    def voltar():
        from modulos.rotas import home_page

        st.switch_page(home_page)

    # Função para visualizar detalhes do financeiro
    def visualizar(financeiro):
        st.session_state["financeiro_id"] = financeiro.pessoa_id

        from modulos.rotas import (
            view_financeiro_page,
        )

        st.switch_page(view_financeiro_page)

    renderizarListagem(
        itens=listaFinanceiros,
        categoria="Listagem",
        titulo="Financeiro",
        descricao=(
            "Consulte os funcionários responsáveis " "pelas operações financeiras."
        ),
        singular="funcionário",
        plural="funcionários",
        colunas=colunas,
        obter_id=lambda financeiro: (financeiro.pessoa_id),
        ao_visualizar=visualizar,
        ao_voltar=voltar,
        prefixo_chave="financeiro",
        titulo_tabela="Funcionários cadastrados",
        mensagem_vazia=("Nenhum funcionário financeiro foi cadastrado no sistema."),
    )
