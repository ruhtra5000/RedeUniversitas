from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from validate_docbr.CPF import CPF

from database.Conexao import SessionLocal
from database.entidades.Pessoa import Pessoa
from database.entidades.Almoxarife import Almoxarife
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
import database.entidades

# Interface
def telaCadastroAlmoxarife():
    st.title("Cadastro de Almoxarife")


# Service
def criarAlmoxarife(pessoa: Pessoa):
    try:
        if not CPF().validate(pessoa.cpf):
            raise Exception("O CPF disponibilizado não é válido.")
        
        if pessoa.email != "":
            if not validarEmail(pessoa.email):
                raise Exception("O E-mail disponibilizado não é válido.")
            
        if pessoa.telefone != "":
            if not validarTelefone(pessoa.telefone):
                raise Exception("O telefone disponibilizado não é válido.")

        dbCriarAlmoxarife(pessoa)
    
    except SQLAlchemyError:    
        raise


# Dados
def dbCriarAlmoxarife(pessoa: Pessoa):
    with SessionLocal() as session:
        try:
            session.add(pessoa)
            session.commit()
            session.refresh(pessoa)

            almoxarife = Almoxarife(
                pessoa_id = pessoa.id,
            )

            session.add(almoxarife)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise