from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.Conexao import SessionLocal
from database.entidades.Financeiro import Financeiro
from database.entidades.Fornecedor import Fornecedor
from database.entidades.Compra import Compra
import database.entidades
from modulos.estoque.estoque_db import dbAdicionarQtdeProduto 


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


#  _____                                            
# /  __ \                                           
# | /  \/  ___   _ __ ___   _ __   _ __   __ _  ___ 
# | |     / _ \ | '_ ` _ \ | '_ \ | '__| / _` |/ __|
# | \__/\| (_) || | | | | || |_) || |   | (_| |\__ \
#  \____/ \___/ |_| |_| |_|| .__/ |_|    \__,_||___/
#                          | |                      
#                          |_|                      

def dbListarComprasCampus(idCampus: int):
    with SessionLocal() as session:
        query = select(select(Compra)
                .join(Compra.financeiro)
                .where(Financeiro.campus_id == idCampus))
        compras = session.execute(query).scalars().all()

        return compras

def dbListarCompraId(idCompra: int):
    with SessionLocal() as session:
        query = select(Compra).where(Compra.id == idCompra)
        compra = session.execute(query).scalar_one_or_none()

        return compra
    
def dbDefinirDataRecebimento(idCompra: int, dataReceb: date):
    with SessionLocal() as session:
        try:
            query = select(Compra).where(Compra.id == idCompra)
            compra = session.execute(query).scalar_one()

            # Quando a data de recebimento for definida
            # pela primeira vez, atualiza o estoque
            if compra.data_recebimento == None:
                dbAdicionarQtdeProduto(compra.produto_id, compra.qtde)
            
            compra.data_recebimento = dataReceb
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise