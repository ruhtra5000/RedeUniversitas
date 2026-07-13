from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base

if TYPE_CHECKING:
    from database.entidades.Disciplina import Disciplina

class PreRequisito(Base):
    __tablename__ = "prerequisito"

    # Colunas
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplina.id"), primary_key=True)
    prerequisito_id: Mapped[int] = mapped_column(ForeignKey("disciplina.id"), primary_key=True)

    # Ligações de ORM
    disciplina: Mapped["Disciplina"] = relationship(
        foreign_keys=[disciplina_id],
        back_populates="preRequisitos"
    )

    prerequisito: Mapped["Disciplina"] = relationship(
        foreign_keys=[prerequisito_id]
    )