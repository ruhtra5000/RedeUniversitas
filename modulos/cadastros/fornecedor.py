from sqlalchemy.exc import SQLAlchemyError
from validate_docbr.CNPJ import CNPJ

from database.Conexao import SessionLocal
from database.entidades.Fornecedor import Fornecedor
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
import database.entidades

# === Dados recebidos ===
# - fornecedor:
#       nome: str
#       cnpj: str (somente numeros)
#       email: str
#       telefone: str

# Service
def criarFornecedor(fornecedor: Fornecedor):
    try:
        if not CNPJ().validate(fornecedor.cnpj):
            raise Exception("O CNPJ disponibilizado não é válido.")
        
        if not validarEmail(fornecedor.email):
            raise Exception("O E-mail disponibilizado não é válido.")
            
        if not validarTelefone(fornecedor.telefone):
            raise Exception("O telefone disponibilizado não é válido.")

        dbCriarFornecedor(fornecedor)
    
    except SQLAlchemyError:    
        raise


# Dados
def dbCriarFornecedor(fornecedor: Fornecedor):
    with SessionLocal() as session:
        try:
            session.add(fornecedor)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise