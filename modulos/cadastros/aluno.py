from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from validate_docbr.CPF import CPF
from database.Conexao import SessionLocal
import database.entidades
from database.entidades.Pessoa import Pessoa
from database.entidades.Aluno import Aluno
from database.entidades.Campus import Campus
from database.entidades.Curso import Curso
from modulos.cadastros.cadastro_utils import validarEmail, validarTelefone 
from modulos.academico.academico_db import dbExisteCpf, dbExisteEmail


# === Dados recebidos ===
# - pessoa:
#       cpf: str
#       nome: str
#       email: str 
#       telefone: str | None (opcional)
# - idCampus: int
# - idCurso: int

# Service
def criarAluno(pessoa: Pessoa, idCampus: int, idCurso: int):
    try:
        if not CPF().validate(pessoa.cpf):
            raise Exception("O CPF disponibilizado não é válido.")
        
        if dbExisteCpf(pessoa.cpf):
            raise Exception("Já existe um aluno cadastrado com este CPF.")
        
        if not validarEmail(pessoa.email):
            raise Exception("O E-mail disponibilizado não é válido.")
        
        if dbExisteEmail(pessoa.email):
            raise Exception("Já existe um aluno cadastrado com este e-mail.")
            
        if pessoa.telefone is not None and pessoa.telefone != "":
            if not validarTelefone(pessoa.telefone):
                raise Exception("O telefone disponibilizado não é válido.")
                
        dbCriarAluno(pessoa, idCampus, idCurso)
    
    except SQLAlchemyError:    
        raise

    except Exception:
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