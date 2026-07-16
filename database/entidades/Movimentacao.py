from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base
from database.entidades.enums.StatusMovimentacao import StatusMovimentacao

if TYPE_CHECKING:
    from database.entidades.Almoxarife import Almoxarife
    from database.entidades.Estoque import Estoque

class Movimentacao(Base):
    __tablename__ = "movimentacao"

    # Colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    produto_id: Mapped[int] = mapped_column(ForeignKey("estoque.id"))
    pessoa_id: Mapped[int] = mapped_column(ForeignKey("almoxarife.pessoa_id"))
    qtde_mov: Mapped[int] = mapped_column(default=1)
    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    tipo: Mapped["StatusMovimentacao"] = mapped_column(Enum(StatusMovimentacao), nullable=False) 

    # Ligações de ORM
    produto: Mapped["Estoque"] = relationship(
        foreign_keys=[produto_id],
        back_populates="movimentacoes"
    )

    almoxarife: Mapped["Almoxarife"] = relationship(
        foreign_keys=[pessoa_id],
        back_populates="movimentacoes"
    )

    # Constraints da tabela
    __table_args__ = (
        CheckConstraint(
            "qtde_mov > 0", 
            name="ck_movimentacao_qtde_mov"
        ),
    )