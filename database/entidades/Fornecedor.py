from typing import TYPE_CHECKING

from sqlalchemy import  Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base

if TYPE_CHECKING:
    from database.entidades.Compra import Compra

class Fornecedor(Base):
    __tablename__ = "fornecedor"

    # Colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cnpj: Mapped[str] = mapped_column(String(14), unique=True, nullable=False)
    # endereco: ... 
    email: Mapped[str | None] = mapped_column(String(50))
    telefone: Mapped[str | None] = mapped_column(String(25))

    # Ligações de ORM
    compras: Mapped[list["Compra"]] = relationship(
        foreign_keys="Compra.fornecedor_id",
        back_populates="fornecedor"
    )