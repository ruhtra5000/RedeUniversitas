
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.Conexao import SessionLocal
from database.entidades.Almoxarife import Almoxarife
from database.entidades.Estoque import Estoque
from database.entidades.Movimentacao import Movimentacao
from database.entidades.enums.StatusMovimentacao import StatusMovimentacao
import database.entidades 

# ______                   _         _               
# | ___ \                 | |       | |              
# | |_/ / _ __   ___    __| | _   _ | |_   ___   ___ 
# |  __/ | '__| / _ \  / _` || | | || __| / _ \ / __|
# | |    | |   | (_) || (_| || |_| || |_ | (_) |\__ \
# \_|    |_|    \___/  \__,_| \__,_| \__| \___/ |___/

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

def dbAdicionarQtdeProduto(idProduto: int, qtdeAdd: int):
    with SessionLocal() as session:
        query = select(Estoque).where(Estoque.id == idProduto)
        produto = session.execute(query).scalar_one()

        produto.qtde += qtdeAdd

        session.commit()


# ___  ___               _                          _                                  
# |  \/  |              (_)                        | |                                 
# | .  . |  ___  __   __ _  _ __ ___    ___  _ __  | |_   __ _   ___   ___    ___  ___ 
# | |\/| | / _ \ \ \ / /| || '_ ` _ \  / _ \| '_ \ | __| / _` | / __| / _ \  / _ \/ __|
# | |  | || (_) | \ V / | || | | | | ||  __/| | | || |_ | (_| || (__ | (_) ||  __/\__ \
# \_|  |_/ \___/   \_/  |_||_| |_| |_| \___||_| |_| \__| \__,_| \___| \___/  \___||___/

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


#   ___   _                                       _   __       
#  / _ \ | |                                     (_) / _|      
# / /_\ \| | _ __ ___    ___  __  __  __ _  _ __  _ | |_   ___ 
# |  _  || || '_ ` _ \  / _ \ \ \/ / / _` || '__|| ||  _| / _ \
# | | | || || | | | | || (_) | >  < | (_| || |   | || |  |  __/
# \_| |_/|_||_| |_| |_| \___/ /_/\_\ \__,_||_|   |_||_|   \___|

def dbListarAlmoxarifes():
    with SessionLocal() as session:
        query = select(Almoxarife)
        almoxarifes = session.execute(query).scalars().all()

        return almoxarifes
    
def dbListarAlmoxarifeId(idAlmoxarife: int):
    with SessionLocal() as session:
        query = select(Almoxarife).where(Almoxarife.pessoa_id == idAlmoxarife)
        almoxarife = session.execute(query).scalar_one_or_none()

        return almoxarife