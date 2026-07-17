from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.Conexao import SessionLocal
from database.entidades.Aluno import Aluno
from database.entidades.Bolsa import Bolsa
from database.entidades.Campus import Campus
from database.entidades.Curso import Curso
from database.entidades.Disciplina import Disciplina
from database.entidades.Matricula import Matricula
from database.entidades.Mensalidade import Mensalidade
from database.entidades.PreRequisito import PreRequisito
from database.entidades.Professor import Professor 
from database.entidades.Turma import Turma
from database.entidades.enums.StatusBolsa import StatusBolsa
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


# ______  _             _         _  _                    
# |  _  \(_)           (_)       | |(_)                   
# | | | | _  ___   ___  _  _ __  | | _  _ __    __ _  ___ 
# | | | || |/ __| / __|| || '_ \ | || || '_ \  / _` |/ __|
# | |/ / | |\__ \| (__ | || |_) || || || | | || (_| |\__ \
# |___/  |_||___/ \___||_|| .__/ |_||_||_| |_| \__,_||___/
#                         | |                             
#                         |_|                             

def dbListarDisciplinas(idCurso: int):
    with SessionLocal() as session:
        query = select(Disciplina).where(Disciplina.curso_id == idCurso)
        disciplinas = session.execute(query).scalars().all()

        return disciplinas

def dbListarDisciplinaId(idDisciplina: int):
    with SessionLocal() as session:
        query = select(Disciplina).where(Disciplina.id == idDisciplina)
        disciplina = session.execute(query).scalar_one_or_none()

        return disciplina
    
def dbEditarDisciplina(idDisciplina: int, novaDisciplina: Disciplina):
    # São editaveis: nome, carga_horaria, obrigatoria
    with SessionLocal() as session:
        query = select(Disciplina).where(Disciplina.id == idDisciplina)
        disciplina = session.execute(query).scalar_one()

        disciplina.nome = novaDisciplina.nome
        disciplina.carga_horaria = novaDisciplina.carga_horaria
        disciplina.obrigatoria = novaDisciplina.obrigatoria

        session.commit()

def dbAdicionarPreRequisito(preRequisito: PreRequisito):
    with SessionLocal() as session:
        try:
            session.add(PreRequisito)
            session.commit()
        
        except SQLAlchemyError:
            raise

def dbRemoverPreRequisito(preRequisito: PreRequisito):
    with SessionLocal() as session:
        try:
            session.delete(PreRequisito)
            session.commit()
        
        except SQLAlchemyError:
            raise


#  _____                                
# |_   _|                               
#   | |   _   _  _ __  _ __ ___    __ _ 
#   | |  | | | || '__|| '_ ` _ \  / _` |
#   | |  | |_| || |   | | | | | || (_| |
#   \_/   \__,_||_|   |_| |_| |_| \__,_|

def dbListarTurmasProfessor(idProfessor: int, semestre: str):
    with SessionLocal() as session:
        query = select(Turma).where(Turma.professor_id == idProfessor, Turma.semestre == semestre)
        turmas = session.execute(query).scalars().all()

        return turmas
    
def dbListarTurmasCurso(idCurso: int, semestre: str):
    with SessionLocal() as session:
        query = select(Turma).where(Turma.curso_id == idCurso, Turma.semestre == semestre)
        turmas = session.execute(query).scalars().all()

        return turmas
    
def dbListarTurmaId(idTurma: int):
    with SessionLocal() as session:
        query = select(Turma).where(Turma.id == idTurma)
        turma = session.execute(query).scalar_one_or_none()

        return turma

def dbAlterarProfessorTurma(idTurma: int, idNovoProfessor: int):
    with SessionLocal() as session:
        query = select(Turma).where(Turma.id == idTurma)
        turma = session.execute(query).scalar_one()

        turma.professor_id = idNovoProfessor

        session.commit()

# ___  ___        _          _               _             
# |  \/  |       | |        (_)             | |            
# | .  . |  __ _ | |_  _ __  _   ___  _   _ | |  __ _  ___ 
# | |\/| | / _` || __|| '__|| | / __|| | | || | / _` |/ __|
# | |  | || (_| || |_ | |   | || (__ | |_| || || (_| |\__ \
# \_|  |_/ \__,_| \__||_|   |_| \___| \__,_||_| \__,_||___/

def dbListarMatriculaId(idAluno: int, idTurma: int):
    with SessionLocal() as session:
        query = select(Matricula).where(Matricula.aluno_id == idAluno, Matricula.turma_id == idTurma)
        matricula = session.execute(query).scalar_one_or_none()

        return matricula
        
def dbLancarNota1(idAluno: int, idTurma: int, nota: Decimal):
    with SessionLocal() as session:
        matricula = dbListarMatriculaId(idAluno, idTurma)

        if matricula != None:
            matricula.nota1 = nota
            
            session.add(matricula)
            session.commit()
        else:
            raise SQLAlchemyError
        
def dbLancarNota2(idAluno: int, idTurma: int, nota: Decimal):
    with SessionLocal() as session:
        matricula = dbListarMatriculaId(idAluno, idTurma)

        if matricula != None:
            matricula.nota2 = nota

            if matricula.nota1 != -1 and matricula.nota2 != -1:
                # Atualizar Media
                matricula.media = (matricula.nota1 + matricula.nota2) / 2

                # Atualizar Aprovacao
                if matricula.media >= 7:
                    dbDefinirAprovacao(idAluno, idTurma, True)
            
            elif matricula.nota1 == -1 and matricula.nota2 == -1:
                dbDefinirAprovacao(idAluno, idTurma, False)
            
            session.add(matricula)
            session.commit()
        else:
            raise SQLAlchemyError
        
def dbLancarNota3(idAluno: int, idTurma: int, nota: Decimal):
    with SessionLocal() as session:
        matricula = dbListarMatriculaId(idAluno, idTurma)

        if matricula != None:
            matricula.nota3 = nota

            if (matricula.aprovacao == False) or ((matricula.nota1 == -1 or matricula.nota2 == -1) and matricula.nota3 == -1):
               dbDefinirAprovacao(idAluno, idTurma, False)
            else:
                # Atualizar Media
                notas = [matricula.nota1, matricula.nota2, matricula.nota3]
                maiorNota1 = max(notas)
                notas.remove(maiorNota1)
                maiorNota2 = max(notas)

                matricula.media = (maiorNota1 + maiorNota2) / 2

                # Atualizar Aprovacao
                if matricula.media >= 7:
                    dbDefinirAprovacao(idAluno, idTurma, True)
            
            session.add(matricula)
            session.commit()
        else:
            raise SQLAlchemyError
        
def dbLancarNotaFinal(idAluno: int, idTurma: int, nota: Decimal):
    with SessionLocal() as session:
        matricula = dbListarMatriculaId(idAluno, idTurma)

        if matricula != None:
            if matricula.aprovacao == False:
                raise SQLAlchemyError
            else:
                matricula.final = nota

                # Atualizar Media
                antigaMedia = matricula.media

                matricula.media = (antigaMedia + matricula.final) / 2

                # Atualizar Aprovacao
                if matricula.media >= 5:
                    dbDefinirAprovacao(idAluno, idTurma, True)
                else:
                    dbDefinirAprovacao(idAluno, idTurma, False)
            
            session.add(matricula)
            session.commit()
        else:
            raise SQLAlchemyError

def dbDefinirAprovacao(idAluno: int, idTurma: int, aprovacao: bool):
    with SessionLocal() as session:
        matricula = dbListarMatriculaId(idAluno, idTurma)

        if matricula != None:
            matricula.aprovacao = aprovacao

            session.add(matricula)
            session.commit()
        else:
            raise SQLAlchemyError

        
# Soma um valor a frequencia_abs na Matricula
def dbCadastrarPresenca(idAluno: int, idTurma: int, qtdeAulas: int):
    with SessionLocal() as session:
        matricula = dbListarMatriculaId(idAluno, idTurma)

        matricula.frequencia_abs += qtdeAulas

        session.add(matricula)
        session.commit()
        
def dbCalcularFrequenciaRelativa(idAluno: int, idTurma: int, freqRel: float):
    with SessionLocal() as session:
        matricula = dbListarMatriculaId(idAluno, idTurma)

        matricula.frequencia_rel = freqRel

        session.add(matricula)
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
    
def dbListarProfessoresCampus(idCampus: int):
    with SessionLocal() as session:
        query = select(Professor).where(Professor.campus_id == idCampus)
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

 
#   ___   _                      
#  / _ \ | |                     
# / /_\ \| | _   _  _ __    ___  
# |  _  || || | | || '_ \  / _ \ 
# | | | || || |_| || | | || (_) |
# \_| |_/|_| \__,_||_| |_| \___/ 

def dbListarAlunos():
    with SessionLocal() as session:
        query = select(Aluno)
        alunos = session.execute(query).scalars().all()

        return alunos

def dbListarAlunosCampus(idCampus: int):
    with SessionLocal() as session:
        query = select(Aluno).where(Aluno.campus_id == idCampus)
        alunos = session.execute(query).scalars().all()

        return alunos
    
def dbListarAlunosCurso(idCurso: int):
    with SessionLocal() as session:
        query = select(Aluno).where(Aluno.curso_id == idCurso)
        alunos = session.execute(query).scalars().all()

        return alunos
    
def dbListarAlunoId(idAluno: int):
    with SessionLocal() as session:
        query = select(Aluno).where(Aluno.pessoa_id == idAluno)
        aluno = session.execute(query).scalar_one_or_none()

        return aluno
    
def dbAtualizarCoefRendMediaGeral(idAluno: int, coef_rend: float, media_geral: float):
    with SessionLocal() as session:
        query = select(Aluno).where(Aluno.pessoa_id == idAluno)
        aluno = session.execute(query).scalar_one()

        aluno.coef_rend = coef_rend
        aluno.media_geral = media_geral

        session.commit()


# ______         _                  
# | ___ \       | |                 
# | |_/ /  ___  | | ___   __ _  ___ 
# | ___ \ / _ \ | |/ __| / _` |/ __|
# | |_/ /| (_) || |\__ \| (_| |\__ \
# \____/  \___/ |_||___/ \__,_||___/

def dbListarBolsasAluno(idAluno: int):
    with SessionLocal() as session:
        query = select(Bolsa).where(Bolsa.aluno_id == idAluno)
        bolsas = session.execute(query).scalars().all()

        return bolsas

def dbListarBolsasAtivas():
    with SessionLocal() as session:
        query = select(Bolsa).where(Bolsa.status == StatusBolsa.ATIVA)
        bolsas = session.execute(query).scalars().all()

        return bolsas    

def dbListarBolsasAtivasAluno(idAluno: int):
    with SessionLocal() as session:
        query = select(Bolsa).where(Bolsa.aluno_id == idAluno, Bolsa.status == StatusBolsa.ATIVA)
        bolsas = session.execute(query).scalars().all()

        return bolsas

def dbListarBolsaId(idBolsa: int):
    with SessionLocal() as session:
        query = select(Bolsa).where(Bolsa.id == idBolsa)
        bolsa = session.execute(query).scalar_one_or_none()

        return bolsa

def dbEditarBolsa(idBolsa: int, novaBolsa: Bolsa):
    # São editaveis: tipo_bolsa, percentual_desconto, data_fim e status
    with SessionLocal() as session:
        query = select(Bolsa).where(Bolsa.id == idBolsa)
        bolsa = session.execute(query).scalar_one()

        bolsa.tipo_bolsa = novaBolsa.tipo_bolsa
        bolsa.percentual_desconto = novaBolsa.percentual_desconto
        bolsa.data_fim = novaBolsa.data_fim
        bolsa.status = novaBolsa.status

        session.commit()


# ___  ___                          _  _      _             _            
# |  \/  |                         | |(_)    | |           | |           
# | .  . |  ___  _ __   ___   __ _ | | _   __| |  __ _   __| |  ___  ___ 
# | |\/| | / _ \| '_ \ / __| / _` || || | / _` | / _` | / _` | / _ \/ __|
# | |  | ||  __/| | | |\__ \| (_| || || || (_| || (_| || (_| ||  __/\__ \
# \_|  |_/ \___||_| |_||___/ \__,_||_||_| \__,_| \__,_| \__,_| \___||___/

def dbListarMensalidades():
    with SessionLocal() as session:
        query = select(Mensalidade)
        mensalidades = session.execute(query).scalars().all()

        return mensalidades

def dbListarMensalidadesCampus(idCampus: int):
    with SessionLocal() as session:
        query = select(select(Mensalidade)
                .join(Mensalidade.aluno)
                .where(Aluno.campus_id == idCampus))
        
        mensalidades = session.execute(query).scalars().all()

        return mensalidades

def dbListarMensalidadesCurso(idCurso: int):
    with SessionLocal() as session:
        query = select(select(Mensalidade)
                .join(Mensalidade.aluno)
                .where(Aluno.curso_id == idCurso))
        
        mensalidades = session.execute(query).scalars().all()

        return mensalidades

def dbListarMensalidadesAluno(idAluno: int):
    with SessionLocal() as session:
        query = select(select(Mensalidade).where(Mensalidade.aluno_id == idAluno))
        mensalidades = session.execute(query).scalars().all()

        return mensalidades
    
def dbListarMensalidadeId(idMensalidade: int):
    with SessionLocal() as session:
        query = select(select(Mensalidade).where(Mensalidade.id == idMensalidade))
        mensalidade = session.execute(query).scalar_one_or_none()

        return mensalidade
