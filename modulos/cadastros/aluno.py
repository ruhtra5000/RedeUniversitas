from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from validate_docbr.CPF import CPF

from database.Conexao import SessionLocal
from database.entidades.Pessoa import Pessoa
from database.entidades.Aluno import Aluno
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
import database.entidades

# Interface
def telaCadastroAluno():
    st.title("Cadastro de Aluno")


# Service
def criarAluno(pessoa: Pessoa, idCampus: int, idCurso: int):
    try:
        if not CPF().validate(pessoa.cpf):
            raise Exception("O CPF disponibilizado não é válido.")
        
        if not validarEmail(pessoa.email):
            raise Exception("O E-mail disponibilizado não é válido.")
            
        if pessoa.telefone != "":
            if not validarTelefone(pessoa.telefone):
                raise Exception("O telefone disponibilizado não é válido.")

        dbCriarAluno(pessoa, idCampus, idCurso)
    
    except SQLAlchemyError:    
        raise


# Dados
def dbCriarAluno(pessoa: Pessoa, idCampus: int, idCurso: int):
    anoAtual = datetime.now().year

    with SessionLocal() as session:
        try:
            session.add(pessoa)
            session.commit()
            session.refresh(pessoa)

            aluno = Aluno(
                pessoa_id = pessoa.id,
                matricula = f"{anoAtual}-{pessoa.id:05d}",
                campus_id = idCampus,
                curso_id = idCurso
            )

            session.add(aluno)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise