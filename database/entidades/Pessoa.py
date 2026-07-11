from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base

if TYPE_CHECKING:
    from database.entidades.Almoxarife import Almoxarife
    from database.entidades.Aluno import Aluno
    from database.entidades.Financeiro import Financeiro
    from database.entidades.Professor import Professor

class Pessoa(Base):
    __tablename__ = "pessoa"

    # Colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str | None] = mapped_column(String(50), unique=True)
    telefone: Mapped[str | None] = mapped_column(String(25), unique=True)

    # Ligações de ORM
    almoxarife: Mapped["Almoxarife"] = relationship(
        back_populates="pessoa",
        uselist=False
    )

    aluno: Mapped["Aluno"] = relationship(
        back_populates="pessoa",
        uselist=False
    )

    professor: Mapped["Professor"] = relationship(
        back_populates="pessoa",
        uselist=False
    )

    financeiro: Mapped["Financeiro"] = relationship(
        back_populates="pessoa",
        uselist=False
    )