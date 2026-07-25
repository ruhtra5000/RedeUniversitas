from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from validate_docbr.CPF import CPF
from database.Conexao import SessionLocal
from database.entidades.Pessoa import Pessoa
from database.entidades.Financeiro import Financeiro
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
import database.entidades

def telaCadastroFinanceiro():
    st.title("Cadastro de Financeiro")