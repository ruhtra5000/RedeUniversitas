from sqlalchemy.exc import SQLAlchemyError

from database.Conexao import SessionLocal
from database.entidades.Estoque import Estoque
import database.entidades

# === Dados recebidos ===
# - produto:
#       nome: str
#       marca: str
#       qtde: int
#       qtde_min: int
#       campus_id: int

# Service
def criarEstoque(produto: Estoque):
    try:
        dbCriarEstoque(produto)
    
    except Exception:    
        raise


# Dados
def dbCriarEstoque(produto: Estoque):
    with SessionLocal() as session:
        try:
            session.add(produto)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise