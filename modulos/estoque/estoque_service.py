from modulos.estoque.estoque_db import *

# ______                   _         _               
# | ___ \                 | |       | |              
# | |_/ / _ __   ___    __| | _   _ | |_   ___   ___ 
# |  __/ | '__| / _ \  / _` || | | || __| / _ \ / __|
# | |    | |   | (_) || (_| || |_| || |_ | (_) |\__ \
# \_|    |_|    \___/  \__,_| \__,_| \__| \___/ |___/

def listarProdutos(idCampus: int):
    return dbListarProdutos(idCampus)

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

def criarMovimentacao(movimentacao: Movimentacao):
    try:
        dbCriarMovimentacao(movimentacao)

    except SQLAlchemyError:
        raise

def listarMovimentacoes(idCampus: int):
    return dbListarMovimentacoes(idCampus)

def listarMovimentacaoId(idMovimentacao: int):
    movimentacao =  dbListarMovimentacaoId(idMovimentacao)

    if movimentacao == None:
        raise Exception(f"Movimentação com id {idMovimentacao} não existente.")
    
    return movimentacao


#   ___   _                                       _   __       
#  / _ \ | |                                     (_) / _|      
# / /_\ \| | _ __ ___    ___  __  __  __ _  _ __  _ | |_   ___ 
# |  _  || || '_ ` _ \  / _ \ \ \/ / / _` || '__|| ||  _| / _ \
# | | | || || | | | | || (_) | >  < | (_| || |   | || |  |  __/
# \_| |_/|_||_| |_| |_| \___/ /_/\_\ \__,_||_|   |_||_|   \___|

def listarAlmoxarifes():
    return dbListarAlmoxarifes()
    
def listarAlmoxarifeId(idAlmoxarife: int):
    almoxarife = dbListarAlmoxarifeId(idAlmoxarife)

    if almoxarife == None:
        raise Exception(f"Almoxarife com id {idAlmoxarife} não existente.")
    
    return almoxarife