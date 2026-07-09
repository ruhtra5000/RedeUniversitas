from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base

if TYPE_CHECKING:
    from database.entidades.Curso import Curso

class Disciplina(Base):
    __tablename__ = "disciplina"

    # Colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    codigo: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    carga_horaria: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    obrigatoria: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    curso_id: Mapped[int] = mapped_column(ForeignKey("curso.id"))

    # Ligações de ORM
    curso: Mapped["Curso"] = relationship(
        foreign_keys=[curso_id],
        back_populates="disciplinas"
    )

    # Constraints da tabela
    __table_args__ = (
        UniqueConstraint(
            "curso_id",
            "nome",
            name="uq_disciplina_curso_nome"
        ),
    )