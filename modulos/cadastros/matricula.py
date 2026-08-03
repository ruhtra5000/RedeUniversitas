from sqlalchemy.exc import SQLAlchemyError

from database.Conexao import SessionLocal
from database.entidades.Aluno import Aluno
from database.entidades.Disciplina import Disciplina
from database.entidades.Matricula import Matricula
import database.entidades


# === Dados recebidos ===
# - matricula:
#       aluno_id: int
#       turma_id: int
#       disciplina_id: int
#       aluno: Aluno
#       disciplina: Disciplina

# Service
def criarMatricula(matricula: Matricula, aluno: Aluno, disciplina: Disciplina):
    try:
        if aluno.curso_id != disciplina.curso_id:
            raise Exception(f"O aluno deve pertencer ao mesmo curso da disciplina.")
        
        with SessionLocal() as session:
            # Pegamos os pre requisitos da disciplina
            from sqlalchemy import select
            from database.entidades.PreRequisito import PreRequisito
            from database.entidades.Matricula import Matricula as MatrDB
            
            preReqs = session.execute(
                select(PreRequisito).where(PreRequisito.disciplina_id == disciplina.id)
            ).unique().scalars().all()
            
            matrAluno = session.execute(
                select(MatrDB).where(MatrDB.aluno_id == aluno.pessoa_id)
            ).unique().scalars().all()
            
            flag = True
            for preReq in preReqs:
                cursado = False
                for matr in matrAluno:
                    if preReq.prerequisito_id == matr.disciplina_id:
                        cursado = True
                        if matr.aprovacao == None or matr.aprovacao == False:
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
