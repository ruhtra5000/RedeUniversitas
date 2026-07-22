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
    financeiro = dbListarFinanceiroId(idFinanceiro)

    if financeiro == None:
        raise Exception(f"Financeiro com id {idFinanceiro} não existente.")
    
    return financeiro


#  _____                _          ______                    _                 
# /  __ \              | |         | ___ \                  | |                
# | /  \/  ___   _ __  | |_   __ _ | |_/ /  ___   ___   ___ | |__    ___  _ __ 
# | |     / _ \ | '_ \ | __| / _` ||    /  / _ \ / __| / _ \| '_ \  / _ \| '__|
# | \__/\| (_) || | | || |_ | (_| || |\ \ |  __/| (__ |  __/| |_) ||  __/| |   
#  \____/ \___/ |_| |_| \__| \__,_|\_| \_| \___| \___| \___||_.__/  \___||_|   

def listarContasReceber():
    return dbListarContasReceber()

# Lista as contas a receber vencidas por campus (caixa é único por campus)
def listarContasReceberCaixaVencidas(idCaixa: int):
    return dbListarContasReceberCaixaVencidas(idCaixa)
    
def listarContaReceberId(idContaReceber: int):
    contaReceber = dbListarContaReceberId(idContaReceber)

    if contaReceber == None:
        raise Exception(f"ContaReceber com id {idContaReceber} não existente.")
    
    return contaReceber
    
def definirDataPagamentoContaReceber(idContaReceber: int, dataPagamento: date):
    dbDefinirDataPagamentoContaReceber(idContaReceber, dataPagamento)

def definirFinanceiroContaReceber(idContaReceber: int, idFinanceiro: int):
    dbDefinirFinanceiroContaReceber(idContaReceber, idFinanceiro)


#  _____                _          ______                            
# /  __ \              | |         | ___ \                           
# | /  \/  ___   _ __  | |_   __ _ | |_/ / __ _   __ _   __ _  _ __ 
# | |     / _ \ | '_ \ | __| / _` ||  __/ / _` | / _` | / _` || '__|
# | \__/\| (_) || | | || |_ | (_| || |   | (_| || (_| || (_| || |   
#  \____/ \___/ |_| |_| \__| \__,_|\_|    \__,_| \__, | \__,_||_|   
#                                                 __/ |             
#                                                |___/

def listarContasPagar():
    return dbListarContasPagar()
    
# lista as contas a pagar vencidas por campus (caixa é único por campus)
def listarContasPagarCaixaVencidas(idCaixa: int):
    return dbListarContasPagarCaixaVencidas(idCaixa)
    
def listarContaPagarId(idContaPagar: int):
    contaPagar = dbListarContaPagarId(idContaPagar)

    if contaPagar == None:
        raise Exception(f"ContaPagar com id {idContaPagar} não existente.")
    
    return contaPagar

def definirDataPagamentoContaPagar(idContaPagar: int, dataPagamento: date):
    dbDefinirDataPagamentoContaPagar(idContaPagar, dataPagamento)