from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from database.Conexao import SessionLocal
from database.entidades.Bolsa import Bolsa
from modulos.academico.academico_db import dbListarBolsasAtivasAluno
import database.entidades

# === Dados recebidos ===
# - bolsa:
#       aluno_id: int
#       tipo_bolsa: str (descrição basica)
#       percentual_desconto: float (Faixa: [0, 1])
#       data_inicio: date
#       data_fim: date
#       status: StatusBolsa

# Service
def criarBolsa(bolsa: Bolsa, aluno):
    try:
        bolsasAtivas = dbListarBolsasAtivasAluno(bolsa.aluno_id)
        
        if bolsasAtivas == None or bolsasAtivas == []:
            pass
        
        else:
            raise Exception(f"O aluno {aluno.pessoa.nome} já tem uma bolsa ativa vinculada a si.")
        
        if bolsa.data_fim < bolsa.data_inicio:
            raise Exception(f"A data de início deve vir antes da data de fim.")

        dbCriarBolsa(bolsa)
    
    except SQLAlchemyError:    
        raise

    except Exception:
        raise


# Dados
def dbCriarBolsa(bolsa: Bolsa):
    with SessionLocal() as session:
        try:
            session.add(bolsa)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise