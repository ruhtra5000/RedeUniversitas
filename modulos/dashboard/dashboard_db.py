from datetime import date

from sqlalchemy import case, func, or_, select
from sqlalchemy.exc import SQLAlchemyError

from database.Conexao import SessionLocal
from database.entidades.Aluno import Aluno
from database.entidades.Bolsa import Bolsa
from database.entidades.ContaReceber import ContaReceber
from database.entidades.Curso import Curso
from database.entidades.Matricula import Matricula
from database.entidades.Mensalidade import Mensalidade
from database.entidades.Professor import Professor
from database.entidades.enums.StatusAluno import StatusAluno
import database.entidades
from database.entidades.enums.StatusBolsa import StatusBolsa


#  _____                     _ 
# |  __ \                   | |
# | |  \/  ___  _ __   __ _ | |
# | | __  / _ \| '__| / _` || |
# | |_\ \|  __/| |   | (_| || |
#  \____/ \___||_|    \__,_||_|

def dbContarAlunosAtivos(
        idCampus: int | None = None,
        idCurso: int | None = None
    ):
    with SessionLocal() as session:
        query = select(func.count(Aluno.pessoa_id)).where(Aluno.status == StatusAluno.ATIVO)

        if idCampus is not None:
            query = query.where(Aluno.campus_id == idCampus)

        elif idCurso is not None: 
            query = query.where(Aluno.curso_id == idCurso)

        qtdeAlunos = session.scalar(query)

        return qtdeAlunos

def dbContarAlunosFormados(
        idCampus: int | None = None,
        idCurso: int | None = None
    ):
    with SessionLocal() as session:
        query = select(func.count(Aluno.pessoa_id)).where(Aluno.status == StatusAluno.FORMADO)

        if idCampus is not None:
            query = query.where(Aluno.campus_id == idCampus)

        elif idCurso is not None: 
            query = query.where(Aluno.curso_id == idCurso)

        qtdeAlunos = session.scalar(query)

        return qtdeAlunos

def dbContarAlunosEvadidos(
        idCampus: int | None = None,
        idCurso: int | None = None
    ):
    with SessionLocal() as session:
        query = select(func.count(Aluno.pessoa_id)).where(Aluno.status == StatusAluno.EVADIDO)

        if idCampus is not None:
            query = query.where(Aluno.campus_id == idCampus)

        elif idCurso is not None: 
            query = query.where(Aluno.curso_id == idCurso)

        qtdeAlunos = session.scalar(query)

        return qtdeAlunos

def dbCalcularTaxaEvasao():
    with SessionLocal() as session:
        query = select(func.count(Aluno.pessoa_id))
        qtdeTotalAlunos = session.scalar(query)

        qtdeAlunosEvadidos = dbContarAlunosEvadidos()
    
        return (qtdeAlunosEvadidos / qtdeTotalAlunos)

def dbContarProfessores(
        idCampus: int | None = None,
        idCurso: int | None = None
    ):
    with SessionLocal() as session:
        query = select(func.count(Professor.pessoa_id))

        if idCampus is not None:
            query = query.where(Professor.campus_id == idCampus)

        elif idCurso is not None: 
            query = query.where(Professor.curso_id == idCurso)

        qtdeProfessores = session.scalar(query)

        return qtdeProfessores

def dbContarCursos(
        idCampus: int | None = None,
    ):
    with SessionLocal() as session:
        query = select(func.count(Curso.id))

        if idCampus is not None:
            query = query.where(Curso.campus_id == idCampus)

        qtdeCursos = session.scalar(query)

        return qtdeCursos


#   ___                    _                   _              
#  / _ \                  | |                 (_)             
# / /_\ \  ___   __ _   __| |  ___  _ __ ___   _   ___   ___  
# |  _  | / __| / _` | / _` | / _ \| '_ ` _ \ | | / __| / _ \ 
# | | | || (__ | (_| || (_| ||  __/| | | | | || || (__ | (_) |
# \_| |_/ \___| \__,_| \__,_| \___||_| |_| |_||_| \___| \___/ 

def dbCalcularCoefRendMedio(
        idCampus: int | None = None,
        idCurso: int | None = None
    ):
    with SessionLocal() as session:
        query = select(func.avg(Aluno.coef_rend))
    
        if idCampus is not None:
            query = query.where(Aluno.campus_id == idCampus)

        elif idCurso is not None:
            query = query.where(Aluno.curso_id == idCurso)
            
        crMedio = session.scalar(query)
    
        return crMedio

# Retorna a quantidade de alunos em categorias de desempenho
def dbAgruparAlunosDesempenho(
        idCampus: int | None = None,
        idCurso: int | None = None    
    ):
    categoria = case(
        (Aluno.coef_rend >= 8.5, "Excelente"),
        (Aluno.coef_rend >= 7.0, "Bom"),
        (Aluno.coef_rend >= 5.5, "Regular"),
        else_="Ruim"
    )

    with SessionLocal() as session:
        query = (
            select(
                categoria.label("categoria"),
                func.count(Aluno.pessoa_id).label("quantidade")
            )
            .group_by(categoria)
        )

        if idCampus is not None:
            query = query.where(Aluno.campus_id == idCampus)
        
        elif idCurso is not None: 
            query = query.where(Aluno.curso_id == idCurso)

        resultado = session.execute(query).all()

        return resultado

# Baixo desempenho: CR < 5.5 ou 3+ reprovaçoes
def dbAlunosBaixoDesempenho(
        idCampus: int | None = None,
        idCurso: int | None = None 
    ):
    with SessionLocal() as session:
        reprovacoes = (
            select(func.count(Matricula.id))
            .where(
                Matricula.aluno_id == Aluno.pessoa_id,
                Matricula.aprovacao == False
            )
            .scalar_subquery()
        )

        query = select(Aluno).where(
            or_(Aluno.coef_rend < 5.5, reprovacoes >= 3)
        )
    
        if idCampus is not None:
            query = query.where(Aluno.campus_id == idCampus)
            
        elif idCurso is not None: 
            query = query.where(Aluno.curso_id == idCurso)
    
        alunos = session.execute(query).scalars().all()
    
        return alunos


# ______  _                                   _              
# |  ___|(_)                                 (_)             
# | |_    _  _ __    __ _  _ __    ___   ___  _  _ __   ___  
# |  _|  | || '_ \  / _` || '_ \  / __| / _ \| || '__| / _ \ 
# | |    | || | | || (_| || | | || (__ |  __/| || |   | (_) |
# \_|    |_||_| |_| \__,_||_| |_| \___| \___||_||_|    \___/ 

def dbCalcularReceita(
        idCampus: int | None = None,
        idCurso: int | None = None
    ):
    with SessionLocal() as session:
        query = (
            select(func.sum(ContaReceber.valor))
            .join(ContaReceber.mensalidade)
            .join(Mensalidade.aluno)
            .where(ContaReceber.data_pagamento.is_not(None))
        )
        
        if idCampus is not None:
            query = query.where(Aluno.campus_id == idCampus)
    
        elif idCurso is not None:
            query = query.where(Aluno.curso_id == idCurso)
                
        receita = session.scalar(query)
        
        return receita

def dbCalcularTotalAReceber(
        idCampus: int | None = None,
        idCurso: int | None = None
    ):
    with SessionLocal() as session:
        query = (
            select(func.sum(ContaReceber.valor))
            .join(ContaReceber.mensalidade)
            .join(Mensalidade.aluno)
            .where(ContaReceber.data_pagamento.is_(None))
        )
            
        if idCampus is not None:
            query = query.where(Aluno.campus_id == idCampus)
        
        elif idCurso is not None:
            query = query.where(Aluno.curso_id == idCurso)
                    
        receita = session.scalar(query)
            
        return receita

def dbContarAlunosInadimplentes(
        idCampus: int | None = None,
        idCurso: int | None = None
    ):
    hoje = date.today()

    with SessionLocal() as session:
        query = (
            select(func.count(Aluno.pessoa_id.distinct()))
            .join(Aluno.mensalidades)
            .where(
                Mensalidade.data_vencimento < hoje, 
                Mensalidade.foi_paga == False
            )
        )

        if idCampus is not None:
            query = query.where(Aluno.campus_id == idCampus)
        
        elif idCurso is not None: 
            query = query.where(Aluno.curso_id == idCurso)

        qtdeAlunos = session.scalar(query)

        return qtdeAlunos

def dbCalcularTaxaInadimplencia(
        idCampus: int | None = None,
        idCurso: int | None = None
    ):
    with SessionLocal() as session:
        query = select(func.count(Aluno))

        if idCampus is not None:
            query = query.where(Aluno.campus_id == idCampus)
            qtdeInad = dbContarAlunosInadimplentes(idCampus=idCampus)

        elif idCurso is not None: 
            query = query.where(Aluno.curso_id == idCurso)
            qtdeInad = dbContarAlunosInadimplentes(idCurso=idCurso)
            
        else:
            qtdeInad = dbContarAlunosInadimplentes()

        qtdeAlunos = session.scalar(query)

        return (qtdeInad / qtdeAlunos)

def dbCalcularValorTotalInadimplente(
        idCampus: int | None = None,
        idCurso: int | None = None
    ):
    hoje = date.today()

    with SessionLocal() as session:
        query = (
            select(func.sum(Mensalidade.valor))
            .join(Mensalidade.aluno)
            .where(
                Mensalidade.data_vencimento < hoje, 
                Mensalidade.foi_paga == False
            )
        )

        if idCampus is not None:
            query = query.where(Aluno.campus_id == idCampus)
        
        elif idCurso is not None: 
            query = query.where(Aluno.curso_id == idCurso)

        valorTotal = session.scalar(query)

        return valorTotal

def dbContarMensalidadesVencidas(
        idCampus: int | None = None,
        idCurso: int | None = None 
    ):  
    hoje = date.today()

    with SessionLocal() as session:
        query = (
            select(func.count(Mensalidade.id))
            .join(Mensalidade.aluno)
            .where(
                Mensalidade.data_vencimento < hoje, 
                Mensalidade.foi_paga == False
            )
        )

        if idCampus is not None:
            query = query.where(Aluno.campus_id == idCampus)
        
        elif idCurso is not None: 
            query = query.where(Aluno.curso_id == idCurso)

        qtdeTotal = session.scalar(query)

        return qtdeTotal

def dbCalcularDividaMedia(
        idCampus: int | None = None,
        idCurso: int | None = None
    ):
    if idCampus is not None:
        valorTotal = dbCalcularValorTotalInadimplente(idCampus=idCampus)
        qtdeAlunosInad = dbContarAlunosInadimplentes(idCampus=idCampus)
        
    elif idCurso is not None: 
        valorTotal = dbCalcularValorTotalInadimplente(idCurso=idCurso)
        qtdeAlunosInad = dbContarAlunosInadimplentes(idCurso=idCurso)

    else:
        valorTotal = dbCalcularValorTotalInadimplente()
        qtdeAlunosInad = dbContarAlunosInadimplentes()

    return (valorTotal / qtdeAlunosInad)

def dbContarBolsistas(
        idCampus: int | None = None,
        idCurso: int | None = None
    ):
    with SessionLocal() as session:
        query = (
            select(func.count(Aluno.pessoa_id.distinct()))
            .join(Aluno.bolsas)
            .where(Bolsa.status == StatusBolsa.ATIVA)
        )
        
        if idCampus is not None:
            query = query.where(Aluno.campus_id == idCampus)
    
        elif idCurso is not None:
            query = query.where(Aluno.curso_id == idCurso)
                
        qtdeBolsistas = session.scalar(query)
        
        return qtdeBolsistas

def dbCalcularTaxaBolsistas(
        idCampus: int | None = None,
        idCurso: int | None = None
    ):
    if idCampus is not None:
        qtdeAlunos = dbContarAlunosAtivos(idCampus=idCampus)
        qtdeBolsistas = dbContarBolsistas(idCampus=idCampus)

    elif idCurso is not None: 
        qtdeAlunos = dbContarAlunosAtivos(idCurso=idCurso)
        qtdeBolsistas = dbContarBolsistas(idCurso=idCurso)
            
    else:
        qtdeAlunos = dbContarAlunosAtivos()
        qtdeBolsistas = dbContarBolsistas()

    return (qtdeBolsistas / qtdeAlunos)

def dbCalcularValorConcedidoPorBolsas(
        idCampus: int | None = None,
        idCurso: int | None = None
    ):
    with SessionLocal() as session:
        query = (
            select(func.sum(Curso.mensalidade_base * Bolsa.percentual_desconto))
            .join(Bolsa.aluno)
            .join(Aluno.curso)
            .where(
                Bolsa.status == StatusBolsa.ATIVA,
                Aluno.status == StatusAluno.ATIVO
            )
        )
        
        if idCampus is not None:
            query = query.where(Aluno.campus_id == idCampus)
    
        elif idCurso is not None:
            query = query.where(Aluno.curso_id == idCurso)
                
        totalConcedido = session.scalar(query)
        
        return totalConcedido

#  _____                                  _                       _ 
# |  _  |                                (_)                     | |
# | | | | _ __    ___  _ __   __ _   ___  _   ___   _ __    __ _ | |
# | | | || '_ \  / _ \| '__| / _` | / __|| | / _ \ | '_ \  / _` || |
# \ \_/ /| |_) ||  __/| |   | (_| || (__ | || (_) || | | || (_| || |
#  \___/ | .__/  \___||_|    \__,_| \___||_| \___/ |_| |_| \__,_||_|
#        | |                                                        
#        |_|                                                        