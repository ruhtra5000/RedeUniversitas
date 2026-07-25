from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from database.Conexao import SessionLocal
from database.entidades.Bolsa import Bolsa
from modulos.academico.academico_db import dbListarBolsasAtivasAluno
import database.entidades

def telaCadastroBolsa():
    st.title("Cadastro de Bolsa")
    # percentual_desconto deve estar entre [0, 1]