from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.Conexao import SessionLocal
from database.entidades.Caixa import Caixa
from database.entidades.ContaPagar import ContaPagar
from database.entidades.ContaReceber import ContaReceber
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

            if (caixa.valor_caixa < valorDebito):
                raise Exception(f"O valor a ser debitado excede o valor em caixa.")

            caixa.valor_caixa -= valorDebito

            session.commit()

        except Exception:
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
    

#  _____                _          ______                    _                 
# /  __ \              | |         | ___ \                  | |                
# | /  \/  ___   _ __  | |_   __ _ | |_/ /  ___   ___   ___ | |__    ___  _ __ 
# | |     / _ \ | '_ \ | __| / _` ||    /  / _ \ / __| / _ \| '_ \  / _ \| '__|
# | \__/\| (_) || | | || |_ | (_| || |\ \ |  __/| (__ |  __/| |_) ||  __/| |   
#  \____/ \___/ |_| |_| \__| \__,_|\_| \_| \___| \___| \___||_.__/  \___||_|   

def dbListarContasReceber():
    with SessionLocal() as session:
        query = select(ContaReceber)
        contasReceber = session.execute(query).scalars().all()

        return contasReceber

# lista as contas a receber vencidas por campus (caixa é único por campus)
def dbListarContasReceberCaixaVencidas(idCaixa: int):
    hoje = date.today()

    with SessionLocal() as session:
        query = select(ContaReceber).where(ContaReceber.caixa_id == idCaixa, ContaReceber.data_vencimento < hoje)
        contasReceber = session.execute(query).scalars().all()

        return contasReceber
    
def dbListarContaReceberId(idContaReceber: int):
    with SessionLocal() as session:
        query = select(ContaReceber).where(ContaReceber.id == idContaReceber)
        contaReceber = session.execute(query).scalar_one_or_none()

        return contaReceber
    
def dbDefinirDataPagamentoContaReceber(idContaReceber: int, dataPagamento: date):
    with SessionLocal() as session:
        try:
            query = select(ContaReceber).where(ContaReceber.id == idContaReceber)
            contaReceber = session.execute(query).scalar_one()

            if contaReceber.data_pagamento == None:
                # Alterando data de pagamento
                contaReceber.data_pagamento = dataPagamento

                # Alterando mensalidade (sinalizar que foi pago)
                mensalidade = contaReceber.mensalidade
                mensalidade.foi_paga = True

                # Adicionar valor no caixa
                dbAdicionarValorCaixa(contaReceber.caixa_id, contaReceber.valor)

                session.add(mensalidade)
                session.add(contaReceber)
                session.commit()
            else:
                raise Exception("A data de pagamento relativa à esta mensalidade já foi definida.")
        
        except Exception:
            session.rollback()
            raise

def dbDefinirFinanceiroContaReceber(idContaReceber: int, idFinanceiro: int):
    with SessionLocal() as session:
        query = select(ContaReceber).where(ContaReceber.id == idContaReceber)
        contaReceber = session.execute(query).scalar_one()

        contaReceber.financeiro_id = idFinanceiro

        session.commit()


#  _____                _          ______                            
# /  __ \              | |         | ___ \                           
# | /  \/  ___   _ __  | |_   __ _ | |_/ / __ _   __ _   __ _  _ __ 
# | |     / _ \ | '_ \ | __| / _` ||  __/ / _` | / _` | / _` || '__|
# | \__/\| (_) || | | || |_ | (_| || |   | (_| || (_| || (_| || |   
#  \____/ \___/ |_| |_| \__| \__,_|\_|    \__,_| \__, | \__,_||_|   
#                                                 __/ |             
#                                                |___/

def dbListarContasPagar():
    with SessionLocal() as session:
        query = select(ContaPagar)
        contasPagar = session.execute(query).scalars().all()

        return contasPagar
    
# lista as contas a pagar vencidas por campus (caixa é único por campus)
def dbListarContasPagarCaixaVencidas(idCaixa: int):
    hoje = date.today()

    with SessionLocal() as session:
        query = select(ContaPagar).where(ContaPagar.caixa_id == idCaixa, ContaPagar.data_vencimento < hoje)
        contasPagar = session.execute(query).scalars().all()

        return contasPagar
    
def dbListarContaPagarId(idContaPagar: int):
    with SessionLocal() as session:
        query = select(ContaPagar).where(ContaPagar.id == idContaPagar)
        contaPagar = session.execute(query).scalar_one_or_none()

        return contaPagar

def dbDefinirDataPagamentoContaPagar(idContaPagar: int, dataPagamento: date):
    with SessionLocal() as session:
        try:
            query = select(ContaPagar).where(ContaPagar.id == idContaPagar)
            contaPagar = session.execute(query).scalar_one()

            if contaPagar.data_pagamento == None:
                # Alterando data de pagamento
                contaPagar.data_pagamento = dataPagamento

                # Remover valor no caixa
                dbRemoverValorCaixa(contaPagar.caixa_id, contaPagar.valor)

                session.commit()
            else:
                raise Exception("A data de pagamento relativa à esta compra já foi definida.")
        
        except Exception:
            session.rollback()
            raise