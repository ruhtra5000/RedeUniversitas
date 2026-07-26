from sqlalchemy.exc import SQLAlchemyError

from database.Conexao import SessionLocal
from database.entidades.Turma import Turma
import database.entidades
from modulos.academico.academico_db import (dbListarCursos, dbListarDisciplinasGeral, dbListarProfessores)



# Service
def criarTurma(turma: Turma):
    try:
        turma.codigo = ""
        
        if turma.curso_id != turma.disciplina.curso_id:
            raise Exception(f"A disciplina selecionada deve pertencer ao curso {turma.curso.nome}.")

        if turma.curso.campus_id != turma.professor.campus_id:
            raise Exception(f"O professor designado para esta Turma deve pertencer ao Campus {turma.curso.campus.nome}.")
        
        dbCriarTurma(turma)
            
    except SQLAlchemyError:    
        raise
    
    except Exception:
        raise


# Dados
def dbCriarTurma(turma: Turma):
    with SessionLocal() as session:
        try:
            session.add(turma)
            session.commit()
            session.refresh(turma)
            turma.codigo = f"{turma.disciplina.codigo}-{turma.id:05d}"
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise
