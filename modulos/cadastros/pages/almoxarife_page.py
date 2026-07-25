from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from validate_docbr.CPF import CPF
from database.Conexao import SessionLocal
from database.entidades.Pessoa import Pessoa
from database.entidades.Almoxarife import Almoxarife
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
import database.entidades

def telaCadastroAlmoxarife():
    st.title("Cadastro de Almoxarife")
