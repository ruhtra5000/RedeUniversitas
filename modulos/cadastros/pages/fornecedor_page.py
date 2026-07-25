from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from validate_docbr.CNPJ import CNPJ
from database.Conexao import SessionLocal
from database.entidades.Fornecedor import Fornecedor
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
import database.entidades

def telaCadastroFornecedor():
    st.title("Cadastro de Fornecedor")