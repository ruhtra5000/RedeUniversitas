from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base

if TYPE_CHECKING:
    from database.entidades.Curso import Curso
    from database.entidades.Disciplina import Disciplina
    from database.entidades.Matricula import Matricula
    from database.entidades.Professor import Professor

class Turma(Base):
    __tablename__ = "turma"

    # Colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(25), nullable=False)
    semestre: Mapped[str] = mapped_column(String(25), nullable=False)
    curso_id: Mapped[int] = mapped_column(ForeignKey("curso.id"))
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplina.id"))
    professor_id: Mapped[int] = mapped_column(ForeignKey("professor.pessoa_id"))

    # Ligações de ORM
    curso: Mapped["Curso"] = relationship(
        foreign_keys=[curso_id]
    )

    disciplina: Mapped["Disciplina"] = relationship(
        foreign_keys=[disciplina_id]
    )

    professor: Mapped["Professor"] = relationship(
        foreign_keys=[professor_id],
        back_populates="turmas"
    )

    matriculas: Mapped[list["Matricula"]] = relationship(
        foreign_keys="Matricula.turma_id",
        back_populates="turma"
    )

    # Constraints da tabela
    __table_args__ = (
        UniqueConstraint(
            "codigo",
            "semestre",
            name="uq_turma_codigo_semestre"
        ),
    )
    