from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from database.Conexao import SessionLocal
from database.entidades.Almoxarife import Almoxarife
from database.entidades.Estoque import Estoque
from database.entidades.Movimentacao import Movimentacao
from database.entidades.Pessoa import Pessoa 
from database.entidades.enums.StatusMovimentacao import StatusMovimentacao
import database.entidades


# ______                   _         _               
# | ___ \                 | |       | |              
# | |_/ / _ __   ___    __| | _   _ | |_   ___   ___ 
# |  __/ | '__| / _ \  / _` || | | || __| / _ \ / __|
# | |    | |   | (_) || (_| || |_| || |_ | (_) |\__ \
# \_|    |_|    \___/  \__,_| \__,_| \__| \___/ |___/

def dbListarProdutos():
    with SessionLocal() as session:
        query = select(Estoque)
        produtos = session.execute(query).scalars().all()

        return produtos

def dbListarProdutosCampus(idCampus: int):
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

def dbListarMovimentacoes():
    with SessionLocal() as session:
        query = select(Movimentacao)
        movimentacoes = session.execute(query).scalars().all()
    
        return movimentacoes

def dbListarMovimentacoesCampus(idCampus: int):
    with SessionLocal() as session:
        query = select(Movimentacao).join(Movimentacao.produto).where(Estoque.campus_id == idCampus)
        movimentacoes = session.execute(query).scalars().all()
    
        return movimentacoes

def dbListarMovimentacaoId(idMovimentacao: int):
    with SessionLocal() as session:
        query = select(Movimentacao).where(Movimentacao.id == idMovimentacao)
        movimentacao = session.execute(query).scalar_one_or_none()

        return movimentacao
    
def dbCriarMovimentacao(idProduto: int, idAlmoxarife: int, qtde: int, tipo: StatusMovimentacao):
    with SessionLocal() as session:
        try:
            queryProduto = (
                select(Estoque)
                .where(Estoque.id == idProduto)
            )

            produto = session.execute(
                queryProduto
            ).scalar_one_or_none()

            if produto is None:
                raise Exception(
                    f"Produto com id {idProduto} não existente."
                )

            queryAlmoxarife = (
                select(Almoxarife)
                .where(
                    Almoxarife.pessoa_id == idAlmoxarife
                )
            )

            almoxarife = session.execute(
                queryAlmoxarife
            ).scalar_one_or_none()

            if almoxarife is None:
                raise Exception(
                    f"Almoxarife com id {idAlmoxarife} não existente."
                )

            if qtde <= 0:
                raise Exception(
                    "A quantidade deve ser maior que zero."
                )

            if produto.campus_id != almoxarife.campus_id:
                raise Exception(
                    "O almoxarife não pode realizar movimentações "
                    "em produtos de outro campus."
                )

            if tipo == StatusMovimentacao.ENTRADA:
                produto.qtde += qtde

            elif tipo == StatusMovimentacao.SAIDA:
                if produto.qtde < qtde:
                    raise Exception(
                        "Quantidade insuficiente em estoque."
                    )

                produto.qtde -= qtde

            elif tipo == StatusMovimentacao.PERDA:
                if produto.qtde < qtde:
                    raise Exception(
                        "A quantidade da perda é maior que "
                        "o estoque disponível."
                    )

                produto.qtde -= qtde

            elif tipo == StatusMovimentacao.AJUSTE:
                produto.qtde = qtde

            movimentacao = Movimentacao(
                produto_id=idProduto,
                pessoa_id=idAlmoxarife,
                qtde_mov=qtde,
                tipo=tipo,
            )

            session.add(
                movimentacao
            )

            session.commit()

            session.refresh(
                movimentacao
            )

            return movimentacao

        except Exception:
            session.rollback()
            raise


#   ___   _                                       _   __       
#  / _ \ | |                                     (_) / _|      
# / /_\ \| | _ __ ___    ___  __  __  __ _  _ __  _ | |_   ___ 
# |  _  || || '_ ` _ \  / _ \ \ \/ / / _` || '__|| ||  _| / _ \
# | | | || || | | | | || (_) | >  < | (_| || |   | || |  |  __/
# \_| |_/|_||_| |_| |_| \___/ /_/\_\ \__,_||_|   |_||_|   \___|

def dbListarAlmoxarifes():
    with SessionLocal() as session:
        query = select(Almoxarife).order_by(Almoxarife.pessoa_id)
        almoxarifes = session.execute(query).scalars().all()

        return almoxarifes

def dbListarAlmoxarifesCampus(idCampus: int):
    with SessionLocal() as session:
        query = select(Almoxarife).where(Almoxarife.campus_id == idCampus)
        almoxarifes = session.execute(query).scalars().all()
    
        return almoxarifes
    
def dbListarAlmoxarifeId(idAlmoxarife: int):
    with SessionLocal() as session:
        query = select(Almoxarife).where(Almoxarife.pessoa_id == idAlmoxarife)
        almoxarife = session.execute(query).scalar_one_or_none()

        return almoxarife

def dbListarAlmoxarifeCpf(cpfAlmoxarife: str):
    with SessionLocal() as session:
        query = select(Almoxarife).join(Almoxarife.pessoa).where(Pessoa.cpf == cpfAlmoxarife)
        almoxarife = session.execute(query).scalar_one_or_none()

        return almoxarife