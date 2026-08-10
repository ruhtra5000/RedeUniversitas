import streamlit as st
from modulos.estoque.estoque_service import listarProdutos
from modulos.utils.listagem_utils import formatar_estoque
from modulos.utils.listagem_visual import ColunaListagem, renderizarListagem

# Tela de listagem para Produtos
def telaListagemProdutos():

    listaProdutos = listarProdutos()

    colunas = [
        ColunaListagem(
            titulo="Produto",
            valor=lambda produto: produto.nome,
            subtitulo="Produto em estoque",
            proporcao=2.7,
            tipo="principal",
        ),
        ColunaListagem(
            titulo="Marca",
            valor=lambda produto: (produto.marca or "Não informada"),
            proporcao=1.8,
        ),
        ColunaListagem(
            titulo="Estoque",
            valor=lambda produto: formatar_estoque(produto),
            proporcao=1.8,
            tipo="badge",
        ),
        ColunaListagem(
            titulo="Campus",
            valor=lambda produto: (
                produto.campus.nome if produto.campus else "Não informado"
            ),
            proporcao=2.8,
        ),
    ]

    # Função de navegação
    def voltar():
        from modulos.rotas import home_page

        st.switch_page(home_page)

    # Função para visualizar detalhes do produto
    def visualizar(produto):
        st.session_state["produto_selecionado"] = produto.id

        from modulos.rotas import view_produto_page

        st.switch_page(view_produto_page)

    renderizarListagem(
        itens=listaProdutos,
        categoria="Listagem",
        titulo="Produtos",
        descricao=(
            "Consulte os produtos disponíveis, suas " "marcas, quantidades e campus."
        ),
        singular="produto",
        plural="produtos",
        colunas=colunas,
        obter_id=lambda produto: produto.id,
        ao_visualizar=visualizar,
        ao_voltar=voltar,
        prefixo_chave="produto",
        titulo_tabela="Produtos cadastrados",
        mensagem_vazia=("Nenhum produto foi cadastrado no estoque."),
    )
