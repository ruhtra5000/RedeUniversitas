from modulos.estoque.estoque_db import *

def listarProdutos(idCampus: int):
    return dbListarProdutos(idCampus)

def listarProdutoId(idProduto: int):
    return dbListarProdutoId(idProduto)

def listarProdutosNome(nomeProduto: str):
    return dbListarProdutosNome(nomeProduto)

def editarProduto(idProduto: int, nome: str, marca: str, qtde_min: int):
    try:
        produto = Estoque(
            nome=nome,
            marca=marca,
            qtde_min=qtde_min
        )
        dbEditarProduto(idProduto, produto)

    except SQLAlchemyError:
        raise

def criarMovimentacao(movimentacao: Movimentacao):
    try:
        dbCriarMovimentacao(movimentacao)

    except SQLAlchemyError:
        raise

def listarMovimentacoes(idCampus: int):
    return dbListarMovimentacoes(idCampus)

def listarMovimentacaoId(idMovimentacao: int):
    return dbListarMovimentacaoId(idMovimentacao)