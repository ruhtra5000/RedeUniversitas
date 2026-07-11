from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from validate_docbr.CPF import CPF

from database.Conexao import SessionLocal
from database.entidades.Pessoa import Pessoa
from database.entidades.Professor import Professor
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
import database.entidades

# Interface
def telaCadastroProfessor():
    st.title("Cadastro de Professor")


# Service
def criarProfessor(pessoa: Pessoa, idCampus: int):
    try:
        if not CPF().validate(pessoa.cpf):
            raise Exception("O CPF disponibilizado não é válido.")
        
        if pessoa.email != "":
            if not validarEmail(pessoa.email):
                raise Exception("O E-mail disponibilizado não é válido.")
            
        if pessoa.telefone != "":
            if not validarTelefone(pessoa.telefone):
                raise Exception("O telefone disponibilizado não é válido.")

        dbCriarProfessor(pessoa, idCampus)
    
    except SQLAlchemyError:    
        raise


# Dados
def dbCriarProfessor(pessoa: Pessoa, idCampus: int):
    with SessionLocal() as session:
        try:
            session.add(pessoa)
            session.commit()
            session.refresh(pessoa)

            professor = Professor(
                pessoa_id = pessoa.id,
                campus_id = idCampus
            )

            session.add(professor)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise