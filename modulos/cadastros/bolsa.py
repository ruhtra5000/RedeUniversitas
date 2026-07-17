from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
import streamlit as st

from database.Conexao import SessionLocal
from database.entidades.Bolsa import Bolsa
from modulos.academico.academico_db import dbListarBolsasAtivasAluno
import database.entidades

# Interface
def telaCadastroBolsa():
    st.title("Cadastro de Bolsa")
    # percentual_desconto deve estar entre [0, 1]


# Service
def criarBolsa(bolsa: Bolsa):
    try:
        bolsasAtivas = dbListarBolsasAtivasAluno(bolsa.aluno_id)
        
        if bolsasAtivas == None or bolsasAtivas == []:
            raise Exception(f"O aluno {bolsa.aluno.pessoa.nome} já tem uma bolsa ativa vinculada a si.")
        
        if bolsa.data_fim < bolsa.data_inicio:
            raise Exception(f"A data de início deve vir antes da data de fim.")

        dbCriarBolsa(bolsa)
    
    except SQLAlchemyError:    
        raise

    except Exception:
        raise


# Dados
def dbCriarBolsa(bolsa: Bolsa):
    with SessionLocal() as session:
        try:
            session.add(bolsa)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise