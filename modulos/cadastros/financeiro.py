from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from validate_docbr.CPF import CPF

from database.Conexao import SessionLocal
from database.entidades.Pessoa import Pessoa
from database.entidades.Financeiro import Financeiro
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
import database.entidades

# Interface
def telaCadastroFinanceiro():
    st.title("Cadastro de Financeiro")


# Service
def criarFinanceiro(pessoa: Pessoa, idCampus: int):
    try:
        if not CPF().validate(pessoa.cpf):
            raise Exception("O CPF disponibilizado não é válido.")
        
        if not validarEmail(pessoa.email):
            raise Exception("O E-mail disponibilizado não é válido.")
            
        if pessoa.telefone != "":
            if not validarTelefone(pessoa.telefone):
                raise Exception("O telefone disponibilizado não é válido.")

        dbCriarFinanceiro(pessoa, idCampus)
    
    except SQLAlchemyError:    
        raise


# Dados
def dbCriarFinanceiro(pessoa: Pessoa, idCampus: int):
    with SessionLocal() as session:
        try:
            session.add(pessoa)
            session.commit()
            session.refresh(pessoa)

            financeiro = Financeiro(
                pessoa_id = pessoa.id,
                campus_id = idCampus
            )

            session.add(financeiro)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise