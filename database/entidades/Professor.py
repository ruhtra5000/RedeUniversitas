from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base

if TYPE_CHECKING:
    from database.entidades.Pessoa import Pessoa
    from database.entidades.Turma import Turma
    from database.entidades.Campus import Campus    

class Professor(Base):
    __tablename__ = "professor"

    # Colunas
    pessoa_id: Mapped[int] = mapped_column(ForeignKey("pessoa.id"), primary_key=True)
    campus_id: Mapped[int] = mapped_column(ForeignKey("campus.id"))

    # Ligações de ORM
    pessoa: Mapped["Pessoa"] = relationship(
        back_populates="professor"
    )

    turmas: Mapped[list["Turma"]] = relationship(
        foreign_keys="Turma.professor_id",
        back_populates="professor"
    )

    campus: Mapped["Campus"] = relationship(
        foreign_keys=[campus_id],
        back_populates="professores"
    )
