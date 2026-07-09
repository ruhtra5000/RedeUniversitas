from decimal import Decimal
from typing import TYPE_CHECKING


from sqlalchemy import CheckConstraint, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base
from database.entidades.enums.ModalidadeCurso import ModalidadeCurso

if TYPE_CHECKING:
    from database.entidades.Disciplina import Disciplina
    from database.entidades.Professor import Professor

class Curso(Base):
    __tablename__ = "curso"

    # Colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    modalidade: Mapped["ModalidadeCurso"] = mapped_column(Enum(ModalidadeCurso), nullable=False)
    mensalidade_base: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    carga_horaria: Mapped[int] = mapped_column(nullable=False)
    dur_min_semestre: Mapped[int] = mapped_column(nullable=False)
    dur_max_semestre: Mapped[int] = mapped_column(nullable=False)
    campus_id: Mapped[int] = mapped_column(ForeignKey("campus.id"))
    coordenador_id: Mapped[int] = mapped_column(ForeignKey("professor.pessoa_id"))

    # Ligações de ORM
    coordenador: Mapped["Professor"] = relationship(
        foreign_keys=[coordenador_id]
    )

    disciplinas: Mapped[list["Disciplina"]] = relationship(
        foreign_keys="Disciplina.curso_id",
        back_populates="curso"
    )

    # Constraints da tabela
    __table_args__ = (
        CheckConstraint("mensalidade_base > 0", name="ck_curso_mensalidade_base"),
    )