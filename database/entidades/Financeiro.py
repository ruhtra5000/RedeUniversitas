from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base

if TYPE_CHECKING:
    from database.entidades.Campus import Campus
    from database.entidades.Compra import Compra
    from database.entidades.ContaPagar import ContaPagar
    from database.entidades.ContaReceber import ContaReceber
    from database.entidades.Pessoa import Pessoa

class Financeiro(Base):
    __tablename__ = "financeiro"

    # Colunas
    pessoa_id: Mapped[int] = mapped_column(ForeignKey("pessoa.id"), primary_key=True)
    campus_id: Mapped[int] = mapped_column(ForeignKey("campus.id"))

    # Ligações de ORM
    pessoa: Mapped["Pessoa"] = relationship(
        foreign_keys=[pessoa_id],
        back_populates="financeiro"
    )

    campus: Mapped["Campus"] = relationship(
        foreign_keys=[campus_id]
    )

    compras: Mapped[list["Compra"]] = relationship(
        # Lista de compras aprovadas
        foreign_keys="Compra.financeiro_id",
        back_populates="financeiro"
    )

    contasreceber: Mapped[list["ContaReceber"]] = relationship(
        # Lista de recebimentos aprovados
        foreign_keys="ContaReceber.financeiro_id",
        back_populates="financeiro"
    )

    contaspagar: Mapped[list["ContaPagar"]] = relationship(
        # Lista de pagamentos aprovados
        foreign_keys="ContaPagar.financeiro_id",
        back_populates="financeiro"
    )