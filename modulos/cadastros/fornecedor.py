from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from validate_docbr.CNPJ import CNPJ

from database.Conexao import SessionLocal
from database.entidades.Fornecedor import Fornecedor
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
import database.entidades

# Interface
def telaCadastroFornecedor():
    st.title("Cadastro de Fornecedor")


# Service
def criarFornecedor(fornecedor: Fornecedor):
    try:
        if not CNPJ().validate(fornecedor.cnpj):
            raise Exception("O CNPJ disponibilizado não é válido.")
        
        if fornecedor.email != "":
            if not validarEmail(fornecedor.email):
                raise Exception("O E-mail disponibilizado não é válido.")
            
        if fornecedor.telefone != "":
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