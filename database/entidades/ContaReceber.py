from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base

if TYPE_CHECKING:
    from database.entidades.Financeiro import Financeiro
    from database.entidades.Mensalidade import Mensalidade

class ContaReceber(Base):
    __tablename__ = "contareceber"

    # Colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    descricao: Mapped[str] = mapped_column(String(50))
    valor: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    data_vencimento: Mapped[date] = mapped_column(Date, nullable=False)
    data_pagamento: Mapped[date] = mapped_column(Date, nullable=True)
    mensalidade_id: Mapped[int] = mapped_column(ForeignKey("mensalidade.id"))
    caixa_id: Mapped[int] = mapped_column(ForeignKey("caixa.id"))
    financeiro_id: Mapped[int] = mapped_column(ForeignKey("financeiro.pessoa_id"), nullable=True)

    # Ligações de ORM
    mensalidade: Mapped["Mensalidade"] = relationship(
        foreign_keys=[mensalidade_id],
        back_populates="contareceber"
    )

    financeiro: Mapped["Financeiro"] = relationship(
        foreign_keys=[financeiro_id],
        back_populates="contasreceber"
    )

    # Constraints da tabela
    __table_args__ = (
        CheckConstraint("valor >= 0", name="ck_contareceber_valor"),
    )