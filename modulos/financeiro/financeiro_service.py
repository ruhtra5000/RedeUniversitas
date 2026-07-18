from modulos.financeiro.financeiro_db import *

#  _____         _              
# /  __ \       (_)             
# | /  \/  __ _  _ __  __  __ _ 
# | |     / _` || |\ \/ / / _` |
# | \__/\| (_| || | >  < | (_| |
#  \____/ \__,_||_|/_/\_\ \__,_|

def listarCaixas():
    return dbListarCaixas()
    
def listarCaixaId(idCaixa: int):
    caixa = dbListarCaixaId(idCaixa)

    if caixa == None:
        raise Exception(f"Caixa com id {idCaixa} não existente.")
    
    return caixa
    
def adicionarValorCaixa(idCaixa: int, valorDeposito: Decimal):
    dbAdicionarValorCaixa(idCaixa, valorDeposito)

def removerValorCaixa(idCaixa: int, valorDebito: Decimal):
    caixa = listarCaixaId(idCaixa)

    if (caixa.valor_caixa < valorDebito):
        raise Exception(f"O valor a ser debitado excede o valor em caixa.")
    else:
        dbRemoverValorCaixa(idCaixa, valorDebito)


# ______  _                                   _              
# |  ___|(_)                                 (_)             
# | |_    _  _ __    __ _  _ __    ___   ___  _  _ __   ___  
# |  _|  | || '_ \  / _` || '_ \  / __| / _ \| || '__| / _ \ 
# | |    | || | | || (_| || | | || (__ |  __/| || |   | (_) |
# \_|    |_||_| |_| \__,_||_| |_| \___| \___||_||_|    \___/ 

def listarFinanceiro():
    return dbListarFinanceiro()
    
def listarFinanceiroId(idFinanceiro: int):
    return dbListarFinanceiroId(idFinanceiro)