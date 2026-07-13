from sqlalchemy.exc import SQLAlchemyError
import streamlit as st

from database.Conexao import SessionLocal
from database.entidades.Curso import Curso
from database.entidades.Disciplina import Disciplina
from database.entidades.PreRequisito import PreRequisito
from modulos.academico.academico_db import dbListarDisciplinaId
import database.entidades

# Interface
def telaCadastroDisciplina():
    st.title("Cadastro de Disciplina")


# Service
def criarDisciplina(disciplina: Disciplina, preRequisitos: list[int]):
    # Na lista de pre-requisitos, passar o id das disciplinas 
    # que são pre-requisitos para a disciplina sendo criada
    try:
        disciplina.codigo = "" # Código será atualizado em: dbCriarDisciplina

        if preRequisitos:
            for idPreReq in preRequisitos:
                discPreReq = dbListarDisciplinaId(idPreReq)
                
                if discPreReq == None:
                    raise Exception(f"O id {idPreReq} não corresponde a nenhuma disciplina.")
                
                if discPreReq.curso_id != disciplina.curso_id:
                    raise Exception(f"A disciplina base e seu(s) pre-requisito(s) devem pertencer ao mesmo curso.")
        
            dbCriarDisciplina(disciplina, preRequisitos)
        
        else:
            dbCriarDisciplina(disciplina)

            
    except SQLAlchemyError:    
        raise
    
    except Exception:
        raise


# Dados
def dbCriarDisciplina(disciplina: Disciplina):
    with SessionLocal() as session:
        try:
            session.add(disciplina)
            session.commit()
            session.refresh(disciplina)
            
            # Gerar codigo correto
            disciplina.codigo = f"{disciplina.curso_id}-{disciplina.id:05d}"
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise

def dbCriarDisciplina(disciplina: Disciplina, preRequisitos: list[int]):
    with SessionLocal() as session:
        try:
            session.add(disciplina)
            session.commit()
            session.refresh(disciplina)
            
            # Gerar codigo correto
            disciplina.codigo = f"{disciplina.curso_id}-{disciplina.id:05d}"

            # Adicionar Pre-Requisitos
            preReqFinal: list[PreRequisito] = []
            for idPreReq in preRequisitos:
                preReqFinal.append(PreRequisito(
                    disciplina_id=disciplina.id,
                    prerequisito_id=idPreReq
                ))
            
            session.add_all(preReqFinal)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise