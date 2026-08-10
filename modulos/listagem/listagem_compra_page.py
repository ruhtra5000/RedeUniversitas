import streamlit as st
from modulos.compras.compras_service import listarCompras
from modulos.utils.listagem_utils import (formatar_data, formatar_moeda, obter_nome_produto)
from modulos.utils.listagem_visual import ColunaListagem, renderizarListagem

# Tela de listagem para Compras
def telaListagemCompras():

    listaCompras = listarCompras()

    colunas = [
        ColunaListagem(
            titulo="Produto",
            valor=lambda compra: obter_nome_produto(compra),
            subtitulo="Produto adquirido",
            proporcao=2.6,
            tipo="principal",
        ),
        ColunaListagem(
            titulo="Fornecedor",
            valor=lambda compra: (
                compra.fornecedor.nome if compra.fornecedor else "Não informado"
            ),
            proporcao=2.3,
        ),
        ColunaListagem(
            titulo="Quantidade",
            valor=lambda compra: compra.qtde,
            proporcao=1.1,
        ),
        ColunaListagem(
            titulo="Valor total",
            valor=lambda compra: formatar_moeda(compra.valor_unit * compra.qtde),
            proporcao=1.6,
        ),
        ColunaListagem(
            titulo="Data",
            valor=lambda compra: formatar_data(compra.data_compra),
            proporcao=1.4,
        ),
    ]

    # Função de navegação
    def voltar():
        from modulos.rotas import home_page

        st.switch_page(home_page)

    # Função para visualizar detalhes da compra
    def visualizar(compra):
        st.session_state["compra_selecionada"] = compra.id

        from modulos.rotas import view_compra_page

        st.switch_page(view_compra_page)

    renderizarListagem(
        itens=listaCompras,
        categoria="Listagem",
        titulo="Compras",
        descricao=(
            "Consulte os produtos adquiridos, " "fornecedores, valores e datas."
        ),
        singular="compra",
        plural="compras",
        colunas=colunas,
        obter_id=lambda compra: compra.id,
        ao_visualizar=visualizar,
        ao_voltar=voltar,
        prefixo_chave="compra",
        titulo_tabela="Compras registradas",
        mensagem_vazia=("Nenhuma compra foi cadastrada no sistema."),
    )
