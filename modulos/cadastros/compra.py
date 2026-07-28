from datetime import date

from sqlalchemy.exc import SQLAlchemyError

from database.Conexao import SessionLocal
from database.entidades.Compra import Compra
from database.entidades.ContaPagar import ContaPagar
from modulos.estoque.estoque_service import adicionarQtdeProduto
import database.entidades

# === Dados recebidos ===
# - compra:
#       produto_id: int
#       qtde: int
#       valor_unit: Decimal
#       data_compra: date
#       data_recebimento: date | None (opcional)
#       financeiro_id: int (usuário logado)
#       fornecedor_id: int
# - dataVencimentoContaPagar: date 

# Service
def criarCompra(compra: Compra, dataVencimentoContaPagar: date, financeiro: Financeiro):
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

        dbCriarCompraEContaPagar(compra, contaPagar, financeiro)
    
    except Exception:    
        raise


# Dados
def dbCriarCompraEContaPagar(compra: Compra, contaPagar: ContaPagar, financeiro: Financeiro):
    with SessionLocal() as session:
        try:
            session.add(compra)
            session.commit()
            session.refresh(compra)

            contaPagar.compra_id = compra.id
            contaPagar.caixa_id = financeiro.campus.caixa.id
            session.add(contaPagar)
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise