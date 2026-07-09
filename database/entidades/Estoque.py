from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base

if TYPE_CHECKING:
    from database.entidades.Campus import Campus
    from database.entidades.Compra import Compra

class Estoque(Base):
    __tablename__ = "estoque"

    # Colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    marca: Mapped[str] = mapped_column(String(50), nullable=False)
    qtde: Mapped[int] = mapped_column(default=0)
    qtde_min: Mapped[int] = mapped_column(default=0)
    campus_id: Mapped[int] = mapped_column(ForeignKey("campus.id"))

    # Ligações de ORM
    campus: Mapped["Campus"] = relationship(
        back_populates="estoque"
    )

    compras: Mapped[list["Compra"]] = relationship(
        foreign_keys="Compra.produto_id",
        back_populates="produto"
    )

    # Constraints da tabela
    __table_args__ = (
        CheckConstraint("qtde >= 0", name="ck_estoque_qtde"),
        CheckConstraint("qtde_min >= 0", name="ck_estoque_qtde_min"),
    )
