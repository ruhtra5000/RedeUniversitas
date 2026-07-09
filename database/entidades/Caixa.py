from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base

if TYPE_CHECKING:
    from database.entidades.Campus import Campus
    from database.entidades.ContaPagar import ContaPagar
    from database.entidades.ContaReceber import ContaReceber

class Caixa(Base):
    __tablename__ = "caixa"

    # Colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    valor_caixa: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    campus_id: Mapped[int] = mapped_column(ForeignKey("campus.id"))

    # Ligações de ORM
    campus: Mapped["Campus"] = relationship(
        foreign_keys=[campus_id],
        back_populates="caixa"
    )

    contaspagar: Mapped[list["ContaPagar"]] = relationship(
        foreign_keys="ContaPagar.caixa_id"
    )

    contasreceber: Mapped[list["ContaReceber"]] = relationship(
        foreign_keys="ContaReceber.caixa_id"
    )

    # Constraints da tabela
    __table_args__ = (
        CheckConstraint("valor_caixa >= 0", name="ck_caixa_valor_caixa"),
    )