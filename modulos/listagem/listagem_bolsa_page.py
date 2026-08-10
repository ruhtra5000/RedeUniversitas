import streamlit as st
from modulos.academico.academico_service import listarBolsasGeral
from modulos.utils.listagem_utils import (formatar_data, formatar_percentual, formatar_status)
from modulos.utils.listagem_visual import ColunaListagem, renderizarListagem

# Tela de listagem para Bolsas
def telaListagemBolsas():

    listaBolsas = listarBolsasGeral()

    colunas = [
        ColunaListagem(
            titulo="Aluno",
            valor=lambda bolsa: (bolsa.aluno.pessoa.nome),
            subtitulo="Beneficiário",
            proporcao=2.5,
            tipo="principal",
        ),
        ColunaListagem(
            titulo="Tipo",
            valor=lambda bolsa: getattr(
                bolsa.tipo_bolsa,
                "value",
                bolsa.tipo_bolsa,
            ),
            proporcao=1.8,
        ),
        ColunaListagem(
            titulo="Desconto",
            valor=lambda bolsa: formatar_percentual(bolsa.percentual_desconto),
            proporcao=1.2,
        ),
        ColunaListagem(
            titulo="Início",
            valor=lambda bolsa: formatar_data(bolsa.data_inicio),
            proporcao=1.3,
        ),
        ColunaListagem(
            titulo="Status",
            valor=lambda bolsa: formatar_status(bolsa.status),
            proporcao=1.7,
            tipo="badge",
        ),
    ]

    # Função de navegação
    def voltar():
        from modulos.rotas import home_page

        st.switch_page(home_page)

    # Função para visualizar detalhes da bolsa
    def visualizar(bolsa):
        st.session_state["bolsa_id"] = bolsa.id

        from modulos.rotas import view_bolsa_page

        st.switch_page(view_bolsa_page)

    renderizarListagem(
        itens=listaBolsas,
        categoria="Listagem",
        titulo="Bolsas",
        descricao=(
            "Consulte os benefícios concedidos aos " "alunos e acompanhe seus status."
        ),
        singular="bolsa",
        plural="bolsas",
        colunas=colunas,
        obter_id=lambda bolsa: bolsa.id,
        ao_visualizar=visualizar,
        ao_voltar=voltar,
        prefixo_chave="bolsa",
        titulo_tabela="Bolsas cadastradas",
        mensagem_vazia=("Nenhuma bolsa foi cadastrada no sistema."),
    )
