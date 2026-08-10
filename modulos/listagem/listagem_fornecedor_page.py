import streamlit as st
from modulos.compras.compras_service import listarFornecedores
from modulos.utils.listagem_utils import formatar_cnpj
from modulos.utils.listagem_visual import ColunaListagem, renderizarListagem

# Tela de listagem para Fornecedores
def telaListagemFornecedores():

    listaFornecedores = listarFornecedores()

    colunas = [
        ColunaListagem(
            titulo="Fornecedor",
            valor=lambda fornecedor: fornecedor.nome,
            subtitulo="Fornecedor",
            proporcao=2.6,
            tipo="principal",
        ),
        ColunaListagem(
            titulo="CNPJ",
            valor=lambda fornecedor: formatar_cnpj(fornecedor.cnpj),
            proporcao=2,
        ),
        ColunaListagem(
            titulo="E-mail",
            valor=lambda fornecedor: (fornecedor.email or "Não informado"),
            proporcao=2.7,
        ),
        ColunaListagem(
            titulo="Telefone",
            valor=lambda fornecedor: (fornecedor.telefone or "Não informado"),
            proporcao=1.8,
        ),
    ]

    # Função de navegação
    def voltar():
        from modulos.rotas import home_page

        st.switch_page(home_page)

    # Função para visualizar detalhes do fornecedor
    def visualizar(fornecedor):
        st.session_state["fornecedor_selecionado"] = fornecedor.id

        from modulos.rotas import (
            view_fornecedor_page,
        )

        st.switch_page(view_fornecedor_page)

    renderizarListagem(
        itens=listaFornecedores,
        categoria="Listagem",
        titulo="Fornecedores",
        descricao=(
            "Consulte as empresas fornecedoras e " "suas informações de contato."
        ),
        singular="fornecedor",
        plural="fornecedores",
        colunas=colunas,
        obter_id=lambda fornecedor: fornecedor.id,
        ao_visualizar=visualizar,
        ao_voltar=voltar,
        prefixo_chave="fornecedor",
        titulo_tabela="Fornecedores cadastrados",
        mensagem_vazia=("Nenhum fornecedor foi cadastrado no sistema."),
    )
