from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.Conexao import SessionLocal
from database.entidades.Campus import Campus
from database.entidades.Curso import Curso
from database.entidades.Professor import Professor 
import database.entidades

#  _____                                      
# /  __ \                                     
# | /  \/  __ _  _ __ ___   _ __   _   _  ___ 
# | |     / _` || '_ ` _ \ | '_ \ | | | |/ __|
# | \__/\| (_| || | | | | || |_) || |_| |\__ \
#  \____/ \__,_||_| |_| |_|| .__/  \__,_||___/
#                          | |                
#                          |_|                
       
def dbListarCampus():
    with SessionLocal() as session:
        query = select(Campus)
        campus = session.execute(query).scalars().all()

        return campus

def dbListarCampusId(idCampus: int):
    with SessionLocal() as session:
        query = select(Campus).where(Campus.id == idCampus)
        campus = session.execute(query).scalar_one_or_none()

        return campus

def dbListarCampusNome(nomeCampus: str):
    with SessionLocal() as session:
        query = select(Campus).where(Campus.nome.ilike(f"%{nomeCampus}%"))
        campus = session.execute(query).scalars().all()

        return campus

def dbEditarCampus(idCampus: int, novoCampus: Campus):
    # São editaveis: nome, email e telefone
    with SessionLocal() as session:
        query = select(Campus).where(Campus.id == idCampus)
        campus = session.execute(query).scalar_one_or_none()

        campus.nome = novoCampus.nome
        campus.email = novoCampus.email
        campus.telefone = novoCampus.telefone

        session.commit()

def dbDefinirReitor(idCampus: int, idReitor: int):
    with SessionLocal() as session:
        query = select(Campus).where(Campus.id == idCampus)
        campus = session.execute(query).scalar_one()

        campus.reitor_id = idReitor
        session.commit()

def dbRemoverReitor(idCampus: int):
    with SessionLocal() as session:
        query = select(Campus).where(Campus.id == idCampus)
        campus = session.execute(query).scalar_one()

        campus.reitor_id = None
        session.commit()


#  _____                               
# /  __ \                              
# | /  \/ _   _  _ __  ___   ___   ___ 
# | |    | | | || '__|/ __| / _ \ / __|
# | \__/\| |_| || |   \__ \| (_) |\__ \
#  \____/ \__,_||_|   |___/ \___/ |___/

def dbListarCursos():
    with SessionLocal() as session:
        query = select(Curso)
        cursos = session.execute(query).scalars().all()

        return cursos

def dbListarCursoId(idCurso: int):
    with SessionLocal() as session:
        query = select(Curso).where(Curso.id == idCurso)
        curso = session.execute(query).scalar_one_or_none()

        return curso
    
def dbEditarCurso(idCurso: int, novoCurso: Curso):
    # São editaveis: nome, modalidade, mensalidade_base, carga_horaria,
    #                dur_min_semestre, dur_max_semestre
    with SessionLocal() as session:
        query = select(Curso).where(Curso.id == idCurso)
        curso = session.execute(query).scalar_one()

        curso.nome = novoCurso.nome
        curso.modalidade = novoCurso.modalidade
        curso.mensalidade_base = novoCurso.mensalidade_base
        curso.carga_horaria = novoCurso.carga_horaria
        curso.dur_min_semestre = novoCurso.dur_min_semestre
        curso.dur_max_semestre = novoCurso.dur_max_semestre

        session.commit()
        
def dbDefinirCoordenador(idCurso: int, idCoordenador: int):
    with SessionLocal() as session:
        query = select(Curso).where(Curso.id == idCurso)
        curso = session.execute(query).scalar_one()

        curso.coordenador_id = idCoordenador
        session.commit()

def dbRemoverCoordenador(idCurso: int):
    with SessionLocal() as session:
        query = select(Curso).where(Curso.id == idCurso)
        curso = session.execute(query).scalar_one()

        curso.coordenador_id = None
        session.commit()


# ______                __                                         
# | ___ \              / _|                                        
# | |_/ / _ __   ___  | |_   ___  ___  ___   ___   _ __   ___  ___ 
# |  __/ | '__| / _ \ |  _| / _ \/ __|/ __| / _ \ | '__| / _ \/ __|
# | |    | |   | (_) || |  |  __/\__ \\__ \| (_) || |   |  __/\__ \
# \_|    |_|    \___/ |_|   \___||___/|___/ \___/ |_|    \___||___/
                                                                 
def dbListarProfessores():
    with SessionLocal() as session:
        query = select(Professor)
        professores = session.execute(query).scalars().all()

        return professores
    
def dbListarProfessorId(idProfessor: int):
    with SessionLocal() as session:
        query = select(Professor).where(Professor.pessoa_id == idProfessor)
        professor = session.execute(query).scalar_one_or_none()

        return professor
    
def dbListarProfessorNome(nomeProfessor: str):
    with SessionLocal() as session:
        query = select(Professor).where(Professor.pessoa.nome.ilike(f"%{nomeProfessor}%"))
        professor = session.execute(query).scalars().all()

        return professor
    
def dbListarProfessorCpf(cpfProfessor: str):
    with SessionLocal() as session:
        query = select(Professor).where(Professor.pessoa.cpf.ilike(f"%{cpfProfessor}%"))
        professor = session.execute(query).scalars().all()

        return professor