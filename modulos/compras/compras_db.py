
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.Conexao import SessionLocal
from database.entidades.Fornecedor import Fornecedor
from database.entidades.Compra import Compra
import database.entidades 


# ______                                            _              
# |  ___|                                          | |             
# | |_     ___   _ __  _ __    ___   ___   ___   __| |  ___   _ __ 
# |  _|   / _ \ | '__|| '_ \  / _ \ / __| / _ \ / _` | / _ \ | '__|
# | |    | (_) || |   | | | ||  __/| (__ |  __/| (_| || (_) || |   
# \_|     \___/ |_|   |_| |_| \___| \___| \___| \__,_| \___/ |_|   

def dbListarFornecedores():
    with SessionLocal() as session:
        query = select(Fornecedor)
        fornecedores = session.execute(query).scalars().all()

        return fornecedores
    
def dbListarFornecedoresNome(nomeFornecedor: str):
    with SessionLocal() as session:
        query = select(Fornecedor).where(Fornecedor.nome.ilike(f"%{nomeFornecedor}%"))
        fornecedores = session.execute(query).scalars().all()

        return fornecedores
    
def dbListarFornecedorCnpj(cnpjFornecedor: str):
    with SessionLocal() as session:
        query = select(Fornecedor).where(Fornecedor.cnpj == cnpjFornecedor)
        fornecedor = session.execute(query).scalar_one_or_none()

        return fornecedor
    
def dbListarFornecedorId(idFornecedor: int):
    with SessionLocal() as session:
        query = select(Fornecedor).where(Fornecedor.id == idFornecedor)
        fornecedor = session.execute(query).scalar_one_or_none()

        return fornecedor
    
def dbEditarFornecedor(idFornecedor: int, novoFornecedor: Fornecedor):
    # Só são editaveis: nome, email e telefone
    with SessionLocal() as session:
        try:
            query = select(Fornecedor).where(Fornecedor.id == idFornecedor)
            fornecedor = session.execute(query).scalar_one()

            fornecedor.nome = novoFornecedor.nome
            fornecedor.email = novoFornecedor.email
            fornecedor.telefone = novoFornecedor.telefone

            session.commit()
        
        except SQLAlchemyError:
            session.rollback()
            raise