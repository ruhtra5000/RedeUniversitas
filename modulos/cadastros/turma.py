from sqlalchemy.exc import SQLAlchemyError

from database.Conexao import SessionLocal
from database.entidades.Turma import Turma
import database.entidades


# === Dados recebidos ===
# - turma:
#       semestre: str
#       curso_id: int
#       disciplina_id: int
#       professor_id: int
#       curso: Curso
#       disciplina: Disciplina
#       professor: Professor

# Service
def criarTurma(turma: Turma, curso, disciplina, professor):
    try:
        
        if curso.id != disciplina.curso_id:
            raise Exception(f"A disciplina selecionada deve pertencer ao curso {curso.nome}.")

        if curso.campus_id != professor.campus_id:
            raise Exception(f"O professor designado para esta Turma deve pertencer ao Campus {curso.campus.nome}.")
        
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
