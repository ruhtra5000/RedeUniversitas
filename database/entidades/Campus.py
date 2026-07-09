from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base

if TYPE_CHECKING:
    from database.entidades.Caixa import Caixa
    from database.entidades.Curso import Curso
    from database.entidades.Estoque import Estoque
    from database.entidades.Professor import Professor

class Campus(Base):
    __tablename__ = "campus"

    # Colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cnpj: Mapped[str] = mapped_column(String(14), unique=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    # endereco: ... 
    email: Mapped[str | None] = mapped_column(String(50))
    telefone: Mapped[str | None] = mapped_column(String(25))
    reitor_id: Mapped[int] = mapped_column(ForeignKey("professor.pessoa_id"))

    # Ligações de ORM
    reitor: Mapped["Professor"] = relationship(
        foreign_keys=[reitor_id]
    )

    professores: Mapped[list["Professor"]] = relationship(
        foreign_keys="Professor.campus_id",
        back_populates="campus"
    )

    cursos: Mapped[list["Curso"]] = relationship(
        foreign_keys="Curso.campus_id",
        back_populates="campus"
    )

    estoque: Mapped[list["Estoque"]] = relationship(
        foreign_keys="Estoque.campus_id",
        back_populates="campus"
    )

    caixa: Mapped["Caixa"] = relationship(
        foreign_keys="Caixa.campus_id",
        back_populates="campus"
    )