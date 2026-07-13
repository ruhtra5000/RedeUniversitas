from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
from validate_docbr.CPF import CPF

from database.Conexao import SessionLocal
from database.entidades.Curso import Curso
from modulos.academico.academico_db import dbListarProfessorId
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
import database.entidades

# Interface
def telaCadastroCurso():
    st.title("Cadastro de Curso")


# Service
def criarCurso(curso: Curso):
    try:
        if curso.coordenador_id != "" or curso.coordenador_id != None:
            coordenador = dbListarProfessorId(curso.coordenador_id)

            # Coordenador do curso deve pertencer ao campus vinculado ao curso
            if coordenador.campus_id != curso.campus_id:
                raise Exception(f"O coordenador do curso deve estar vinculado ao campus {coordenador.campus.nome}.")
        
        dbCriarCurso(curso)
            
    except SQLAlchemyError:    
        raise
    
    except Exception:
        raise


# Dados
def dbCriarCurso(curso: Curso):
    with SessionLocal() as session:
        try:
            session.add(curso)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise