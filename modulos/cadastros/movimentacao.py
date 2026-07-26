from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.Conexao import SessionLocal
from database.entidades.Estoque import Estoque
from database.entidades.Movimentacao import Movimentacao
from database.entidades.enums.StatusMovimentacao import StatusMovimentacao
import database.entidades

# === Dados recebidos ===
# - movimentacao:
#       produto_id: int
#       pessoa_id: int (usuário logado)
#       qtde_mov: int
#       data: datetime
#       tipo: StatusMovimentacao

def criarMovimentacao(movimentacao: Movimentacao):
    try:
        dbCriarMovimentacao(movimentacao)

    except Exception:
        raise

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
                    raise Exception("A quantidade retirada é maior que a quantidade em estoque.")

            session.add(movimentacao)
            session.commit()

        except Exception:
            session.rollback()
            raise