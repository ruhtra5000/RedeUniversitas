from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, Date, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base

if TYPE_CHECKING:
    from database.entidades.Aluno import Aluno
    from database.entidades.ContaReceber import ContaReceber

class Mensalidade(Base):
    __tablename__ = "mensalidade"

    # Colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    aluno_id: Mapped[int] = mapped_column(ForeignKey("aluno.pessoa_id"))
    valor: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    data_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    data_vencimento: Mapped[date] = mapped_column(Date, nullable=False)
    foi_paga: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # Ligações de ORM
    aluno: Mapped["Aluno"] = relationship(
        foreign_keys=[aluno_id],
        back_populates="mensalidades"
    )

    contareceber: Mapped["ContaReceber"] = relationship(
        foreign_keys="ContaReceber.mensalidade_id",
        back_populates="mensalidade"
    )

    # Constraints da tabela
    __table_args__ = (
        CheckConstraint("valor >= 0", name="ck_mensalidade_valor"),
    )