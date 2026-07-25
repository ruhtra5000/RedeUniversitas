from datetime import date

from sqlalchemy.exc import SQLAlchemyError

from database.Conexao import SessionLocal
from database.entidades.Compra import Compra
from database.entidades.ContaPagar import ContaPagar
from modulos.estoque.estoque_service import adicionarQtdeProduto
import database.entidades



# Service
def criarCompra(compra: Compra, dataVencimentoContaPagar: date):
    try:
        if compra.qtde <= 0:
            raise Exception("A quantidade comprada deve ser maior que 0.")
        
        if compra.valor_unit <= 0:
            raise Exception("O valor unitário deve ser maior que 0.")
        
        if dataVencimentoContaPagar < compra.data_compra:
            raise Exception("A data de vencimento deve vir após a data da compra.")

        # Gerando ContaPagar referente a Compra
        contaPagar = ContaPagar(
            descricao = f"{compra.data_compra}: Compra de prod-{compra.produto_id} por financ-{compra.financeiro_id}",
            valor = compra.valor_unit * compra.qtde,
            data_vencimento = dataVencimentoContaPagar,
            financeiro_id = compra.financeiro_id
        )

        dbCriarCompraEContaPagar(compra, contaPagar)
    
    except Exception:    
        raise


# Dados
def dbCriarCompraEContaPagar(compra: Compra, contaPagar: ContaPagar):
    with SessionLocal() as session:
        try:
            session.add(compra)
            session.commit()
            session.refresh(compra)

            contaPagar.compra_id = compra.id
            contaPagar.caixa_id = compra.financeiro.campus.caixa.id,
            session.add(contaPagar)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise