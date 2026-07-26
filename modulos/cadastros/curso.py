from sqlalchemy.exc import SQLAlchemyError
from database.Conexao import SessionLocal
from database.entidades.Curso import Curso
from database.entidades.enums.ModalidadeCurso import ModalidadeCurso
from modulos.academico.academico_db import dbListarProfessorId
import database.entidades

# === Dados recebidos ===
# - curso:
#       nome: str
#       modalidade: ModalidadeCurso
#       mensalidade_base: Decimal
#       carga_horaria: int
#       dur_min_semestre: int
#       dur_max_semestre: int
#       campus_id: int
#       coordenador_id: int | None

# Service
def criarCurso(curso: Curso):
    try:
        if curso.coordenador_id:  
            coordenador = dbListarProfessorId(curso.coordenador_id)

            if not coordenador:
                raise Exception("O ID do Coordenador informado não existe no sistema.")

            if coordenador.campus_id != curso.campus_id:
                raise Exception("O coordenador do curso deve estar vinculado ao mesmo campus do curso.")

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