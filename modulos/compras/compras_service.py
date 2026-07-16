from modulos.compras.compras_db import *

from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 

# ______                                            _              
# |  ___|                                          | |             
# | |_     ___   _ __  _ __    ___   ___   ___   __| |  ___   _ __ 
# |  _|   / _ \ | '__|| '_ \  / _ \ / __| / _ \ / _` | / _ \ | '__|
# | |    | (_) || |   | | | ||  __/| (__ |  __/| (_| || (_) || |   
# \_|     \___/ |_|   |_| |_| \___| \___| \___| \__,_| \___/ |_|   

def listarFornecedores():
    return dbListarFornecedores()
    
def listarFornecedoresNome(nomeFornecedor: str):
    return dbListarFornecedoresNome(nomeFornecedor)
    
def listarFornecedorCnpj(cnpjFornecedor: str):
    fornecedor = dbListarFornecedorCnpj(cnpjFornecedor)

    if fornecedor == None:
        raise Exception(f"Fornecedor com CNPJ {cnpjFornecedor} não existente.")
    
    return fornecedor
    
def listarFornecedorId(idFornecedor: int):
    fornecedor = dbListarFornecedorId(idFornecedor)

    if fornecedor == None:
        raise Exception(f"Fornecedor com id {idFornecedor} não existente.")
    
    return fornecedor
    
def editarFornecedor(idFornecedor: int, nome: str, email: str, telefone: str):
    if email != "":
        if not validarEmail(email):
            raise Exception("O e-mail disponibilizado não é válido.")
            
    if telefone != "":
        if not validarTelefone(telefone):
            raise Exception("O telefone disponibilizado não é válido.")
        
    fornecedor = Fornecedor(
        nome=nome,
        email=email,
        telefone=telefone
    )
    
    dbEditarFornecedor(idFornecedor, fornecedor)
    