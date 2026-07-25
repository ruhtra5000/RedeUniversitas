from datetime import date
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from database.Conexao import SessionLocal
from database.entidades.Compra import Compra
from database.entidades.ContaPagar import ContaPagar
from modulos.estoque.estoque_service import adicionarQtdeProduto
import database.entidades

def telaCadastroCompra():
    st.title("Cadastro de Compra")
    # não definir data de recebimento aqui
    # definir depois para atualizar o estoque 
    # (compras_service -> definirDataRecebimento())