from sqlalchemy.exc import SQLAlchemyError
import streamlit as st

from database.Conexao import SessionLocal
from database.entidades.Matricula import Matricula
import database.entidades

# Interface
def telaCadastroMatricula():
    st.title("Cadastro de Matricula")


# Service
def criarMatricula(matricula: Matricula):
    try:
        if matricula.aluno.curso_id != matricula.disciplina.curso_id:
            raise Exception(f"O aluno deve pertencer ao mesmo curso da disciplina.")
        
        # Checagem de pré-requisitos
        flag = True
        for preReq in matricula.disciplina.preRequisitos:
            cursado = False
            for matr in matricula.aluno.matriculas:
                if preReq.prerequisito_id == matr.disciplina_id:
                    cursado = True
                    if matr.aprovacao == False:
                        flag = False

            if not cursado or not flag:
                raise Exception(f"Algum dos pré-requisitos da disciplina não foi concluído ou cursado.")
        
        dbCriarMatricula(matricula)
            
    except SQLAlchemyError:    
        raise
    
    except Exception:
        raise


# Dados
def dbCriarMatricula(matricula: Matricula):
    with SessionLocal() as session:
        try:
            session.add(matricula)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise
