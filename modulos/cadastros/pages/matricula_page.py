from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from database.Conexao import SessionLocal
from database.entidades.Matricula import Matricula
import database.entidades

def telaCadastroMatricula():
    st.title("Cadastro de Matricula")