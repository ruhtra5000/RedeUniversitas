from datetime import date

from apscheduler.schedulers.background import BackgroundScheduler
from dateutil.relativedelta import relativedelta
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st

from database.Conexao import SessionLocal
from database.entidades.Bolsa import Bolsa
from database.entidades.Mensalidade import Mensalidade
from modulos.academico.academico_service import listarAlunos, listarBolsasAtivasAluno
import database.entidades

# Teoricamente, não é necessária interface para
# a criação de mensalidades, pois elas são geradas
# automaticamente no primeiro dia do mês


# Service
def criarMensalidades():
    try:
        alunos = listarAlunos()
        emissao = date.today()
        vencimento = emissao + relativedelta(months=1)
        
        for aluno in alunos:
            mensalidade = Mensalidade(
                aluno_id = aluno.pessoa_id,
                valor = aluno.curso.mensalidade_base,
                data_inicio = emissao,
                data_vencimento = vencimento
            )

            bolsas: list[Bolsa] = listarBolsasAtivasAluno(aluno.pessoa_id)
            if bolsas != [] and bolsas[0].data_fim >= emissao:
                mensalidade.valor *= bolsas[0].percentual_desconto

            dbCriarMensalidade(mensalidade)
    
    except SQLAlchemyError:    
        raise

    except Exception:
        raise


# Dados
def dbCriarMensalidade(mensalidade: Mensalidade):
    with SessionLocal() as session:
        try:
            session.add(mensalidade)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise


# Geraçao periodica
def geracaoAutomaticaMensalidade():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        criarMensalidades,
        trigger="cron",
        day=1,
        hour=0,
        minute=0,
    )

    scheduler.start()