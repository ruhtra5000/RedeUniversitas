from modulos.estoque.estoque_db import *

# ______                   _         _               
# | ___ \                 | |       | |              
# | |_/ / _ __   ___    __| | _   _ | |_   ___   ___ 
# |  __/ | '__| / _ \  / _` || | | || __| / _ \ / __|
# | |    | |   | (_) || (_| || |_| || |_ | (_) |\__ \
# \_|    |_|    \___/  \__,_| \__,_| \__| \___/ |___/

def listarProdutos():
    return dbListarProdutos()

def listarProdutosCampus(idCampus: int):
    return dbListarProdutosCampus(idCampus)

def listarProdutoId(idProduto: int):
    produto = dbListarProdutoId(idProduto)

    if produto == None:
        raise Exception(f"Produto com id {idProduto} não existente.")
    
    return produto

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

def adicionarQtdeProduto(idProduto: int, qtde: int):
    dbAdicionarQtdeProduto(idProduto, qtde)


# ___  ___               _                          _                                  
# |  \/  |              (_)                        | |                                 
# | .  . |  ___  __   __ _  _ __ ___    ___  _ __  | |_   __ _   ___   ___    ___  ___ 
# | |\/| | / _ \ \ \ / /| || '_ ` _ \  / _ \| '_ \ | __| / _` | / __| / _ \  / _ \/ __|
# | |  | || (_) | \ V / | || | | | | ||  __/| | | || |_ | (_| || (__ | (_) ||  __/\__ \
# \_|  |_/ \___/   \_/  |_||_| |_| |_| \___||_| |_| \__| \__,_| \___| \___/  \___||___/

def listarMovimentacoes():
    return dbListarMovimentacoes()

def listarMovimentacoesCampus(idCampus: int):
    return dbListarMovimentacoesCampus(idCampus)

def listarMovimentacaoId(idMovimentacao: int):
    movimentacao =  dbListarMovimentacaoId(idMovimentacao)

    if movimentacao == None:
        raise Exception(f"Movimentação com id {idMovimentacao} não existente.")
    
    return movimentacao

def criarMovimentacao(idProduto: int, idAlmoxarife: int, qtde: int, tipo: StatusMovimentacao):
    if qtde <= 0:
        raise Exception(
            "A quantidade da movimentação deve ser maior que zero."
        )

    return dbCriarMovimentacao(idProduto=idProduto, idAlmoxarife=idAlmoxarife, qtde=qtde, tipo=tipo)


#   ___   _                                       _   __       
#  / _ \ | |                                     (_) / _|      
# / /_\ \| | _ __ ___    ___  __  __  __ _  _ __  _ | |_   ___ 
# |  _  || || '_ ` _ \  / _ \ \ \/ / / _` || '__|| ||  _| / _ \
# | | | || || | | | | || (_) | >  < | (_| || |   | || |  |  __/
# \_| |_/|_||_| |_| |_| \___/ /_/\_\ \__,_||_|   |_||_|   \___|

def listarAlmoxarifes():
    return dbListarAlmoxarifes()

def listarAlmoxarifesCampus(idCampus: int):
    return dbListarAlmoxarifesCampus(idCampus)
    
def listarAlmoxarifeId(idAlmoxarife: int):
    almoxarife = dbListarAlmoxarifeId(idAlmoxarife)

    if almoxarife == None:
        raise Exception(f"Almoxarife com id {idAlmoxarife} não existente.")
    
    return almoxarife

def listarAlmoxarifeCpf(cpfAlmoxarife: str):
    almoxarife = dbListarAlmoxarifeCpf(cpfAlmoxarife)
    
    if almoxarife == None:
        raise Exception(f"Almoxarife com CPF {cpfAlmoxarife} não existente.")
        
    return almoxarife