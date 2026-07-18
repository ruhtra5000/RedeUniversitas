from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.Conexao import SessionLocal
from database.entidades.Caixa import Caixa
from database.entidades.Financeiro import Financeiro
import database.entidades 

#  _____         _              
# /  __ \       (_)             
# | /  \/  __ _  _ __  __  __ _ 
# | |     / _` || |\ \/ / / _` |
# | \__/\| (_| || | >  < | (_| |
#  \____/ \__,_||_|/_/\_\ \__,_|

def dbListarCaixas():
    # Não sei se é necessária essa função, mas...
    with SessionLocal() as session:
        query = select(Caixa)
        caixas = session.execute(query).scalars().all()

        return caixas
    
def dbListarCaixaId(idCaixa: int):
    with SessionLocal() as session:
        query = select(Caixa).where(Caixa.id == idCaixa)
        caixa = session.execute(query).scalar_one_or_none()

        return caixa
    
def dbAdicionarValorCaixa(idCaixa: int, valorDeposito: Decimal):
    with SessionLocal() as session:
        try:
            query = select(Caixa).where(Caixa.id == idCaixa)
            caixa = session.execute(query).scalar_one()

            caixa.valor_caixa += valorDeposito

            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise

def dbRemoverValorCaixa(idCaixa: int, valorDebito: Decimal):
    with SessionLocal() as session:
        try:
            query = select(Caixa).where(Caixa.id == idCaixa)
            caixa = session.execute(query).scalar_one()

            caixa.valor_caixa -= valorDebito

            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise


# ______  _                                   _              
# |  ___|(_)                                 (_)             
# | |_    _  _ __    __ _  _ __    ___   ___  _  _ __   ___  
# |  _|  | || '_ \  / _` || '_ \  / __| / _ \| || '__| / _ \ 
# | |    | || | | || (_| || | | || (__ |  __/| || |   | (_) |
# \_|    |_||_| |_| \__,_||_| |_| \___| \___||_||_|    \___/ 

def dbListarFinanceiro():
    with SessionLocal() as session:
        query = select(Financeiro)
        financeiros = session.execute(query).scalars().all()

        return financeiros
    
def dbListarFinanceiroId(idFinanceiro: int):
    with SessionLocal() as session:
        query = select(Financeiro).where(Financeiro.pessoa_id == idFinanceiro)
        financeiros = session.execute(query).scalar_one_or_none()

        return financeiros