
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.Conexao import SessionLocal
from database.entidades.Estoque import Estoque
from database.entidades.Movimentacao import Movimentacao
from database.entidades.enums.StatusMovimentacao import StatusMovimentacao
import database.entidades 

# Produtos
def dbListarProdutos(idCampus: int):
    with SessionLocal() as session:
        query = select(Estoque).where(Estoque.campus_id == idCampus)
        produtos = session.execute(query).scalars().all()

        return produtos
    
def dbListarProdutoId(idProduto: int):
    with SessionLocal() as session:
        query = select(Estoque).where(Estoque.id == idProduto)
        produto = session.execute(query).scalar_one_or_none()

        return produto
    
def dbListarProdutosNome(nomeProduto: str):
    with SessionLocal() as session:
        query = select(Estoque).where(Estoque.nome.ilike(f"%{nomeProduto}%"))
        produtos = session.execute(query).scalars().all()

        return produtos
    
def dbEditarProduto(idProduto: int, novoProduto: Estoque):
    # Só são editaveis: nome, marca e qtde_min
    with SessionLocal() as session:
        try:
            query = select(Estoque).where(Estoque.id == idProduto)
            produto = session.execute(query).scalar_one_or_none()

            produto.nome = novoProduto.nome
            produto.marca = novoProduto.marca
            produto.qtde_min = novoProduto.qtde_min

            session.commit()
        
        except SQLAlchemyError:
            session.rollback()
            raise

# Movimentações
def dbCriarMovimentacao(movimentacao: Movimentacao):
    with SessionLocal() as session:
        try:
            query = select(Estoque).where(Estoque.id == movimentacao.produto_id)
            produto = session.execute(query).scalar_one()

            if movimentacao.tipo == StatusMovimentacao.ENTRADA:
                produto.qtde += movimentacao.qtde_mov
            else: 
                if produto.qtde >= movimentacao.qtde_mov:
                    produto.qtde -= movimentacao.qtde_mov
                else:
                    raise SQLAlchemyError

            session.add(movimentacao)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise

def dbListarMovimentacoes(idCampus: int):
    with SessionLocal() as session:
        query = select(Estoque).where(Estoque.campus_id == idCampus)
        produtos = session.execute(query).scalars().all()
        
        movimentacoes = []
        
        for prod in produtos:
            movimentacoes + prod.movimentacoes

        return movimentacoes

def dbListarMovimentacaoId(idMovimentacao: int):
    with SessionLocal() as session:
        query = select(Movimentacao).where(Movimentacao.id == idMovimentacao)
        movimentacao = session.execute(query).scalar_one_or_none()

        return movimentacao


