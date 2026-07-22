from datetime import date

from apscheduler.schedulers.background import BackgroundScheduler
from dateutil.relativedelta import relativedelta
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st

from database.Conexao import SessionLocal
from database.entidades.Bolsa import Bolsa
from database.entidades.ContaReceber import ContaReceber
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
                data_vencimento = vencimento,
                foi_paga = False
            )

            bolsas: list[Bolsa] = listarBolsasAtivasAluno(aluno.pessoa_id)
            if bolsas != [] and bolsas[0].data_fim >= emissao:
                mensalidade.valor *= bolsas[0].percentual_desconto

            # Montando ContaReceber referente a mensalidade
            contaReceber = ContaReceber(
                descricao = f"{emissao.strftime("%d/%m/%Y")}: Mensalidade de {aluno.pessoa.cpf}",
                valor = mensalidade.valor,
                data_vencimento = vencimento,
                caixa_id = aluno.campus.caixa.id
            )

            dbCriarMensalidadeEContaReceber(mensalidade, contaReceber)
    
    except SQLAlchemyError:    
        raise

    except Exception:
        raise


# Dados
def dbCriarMensalidadeEContaReceber(mensalidade: Mensalidade, contaReceber: ContaReceber):
    with SessionLocal() as session:
        try:
            session.add(mensalidade)
            session.commit()
            session.refresh(mensalidade)

            contaReceber.mensalidade_id = mensalidade.id

            session.add(contaReceber)
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