from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base

if TYPE_CHECKING:
    from database.entidades.ContaPagar import ContaPagar
    from database.entidades.Estoque import Estoque
    from database.entidades.Financeiro import Financeiro
    from database.entidades.Fornecedor import Fornecedor

class Compra(Base):
    __tablename__ = "compra"

    # Colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    produto_id: Mapped[int] = mapped_column(ForeignKey("estoque.id"))
    qtde: Mapped[int] = mapped_column(Integer, default=1)
    valor_unit: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    financeiro_id: Mapped[int] = mapped_column(ForeignKey("financeiro.pessoa_id"))
    fornecedor_id: Mapped[int] = mapped_column(ForeignKey("fornecedor.id"))

    # Ligações de ORM
    produto: Mapped["Estoque"] = relationship(
        foreign_keys=[produto_id],
        back_populates="compras"
    )

    financeiro: Mapped["Financeiro"] = relationship(
        foreign_keys=[financeiro_id],
        back_populates="compras"
    )

    fornecedor: Mapped["Fornecedor"] = relationship(
        foreign_keys=[fornecedor_id],
        back_populates="compras"
    )

    contapagar: Mapped["ContaPagar"] = relationship(
        foreign_keys="ContaPagar.compra_id",
        back_populates="compra"
    )
    
    # Constraints da tabela
    __table_args__ = (
        CheckConstraint("qtde >= 1", name="ck_compra_qtde"),
        CheckConstraint("valor_unit > 0", name="ck_compra_valor_unit"),
    )