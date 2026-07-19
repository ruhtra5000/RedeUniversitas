from datetime import date

from sqlalchemy.exc import SQLAlchemyError
import streamlit as st

from database.Conexao import SessionLocal
from database.entidades.Compra import Compra
from modulos.estoque.estoque_service import adicionarQtdeProduto
import database.entidades

# Interface
def telaCadastroCompra():
    st.title("Cadastro de Compra")
    # não definir data de recebimento aqui
    # definir depois para atualizar o estoque 
    # (compras_service -> definirDataRecebimento())


# Service
def criarCompra(compra: Compra):
    try:
        if compra.qtde <= 0:
            raise Exception("A quantidade comprada deve ser maior que 0.")
        
        if compra.valor_unit <= 0:
            raise Exception("O valor unitário deve ser maior que 0.")
        
        compra.data = date.today()

        dbCriarCompra(compra)
    
    except SQLAlchemyError:    
        raise


# Dados
def dbCriarCompra(compra: Compra):
    with SessionLocal() as session:
        try:
            session.add(compra)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise