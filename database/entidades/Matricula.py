from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, Float, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base

if TYPE_CHECKING:
    from database.entidades.Aluno import Aluno
    from database.entidades.Disciplina import Disciplina
    from database.entidades.Turma import Turma

class Matricula(Base):
    __tablename__ = "matricula"

    # Colunas
    aluno_id: Mapped[int] = mapped_column(ForeignKey("aluno.pessoa_id"), primary_key=True)
    turma_id: Mapped[int] = mapped_column(ForeignKey("turma.id"), primary_key=True)
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplina.id"))
    nota1: Mapped[Decimal] = mapped_column(Numeric(4, 2))
    nota2: Mapped[Decimal] = mapped_column(Numeric(4, 2))
    nota3: Mapped[Decimal] = mapped_column(Numeric(4, 2))
    final: Mapped[Decimal] = mapped_column(Numeric(4, 2))
    media: Mapped[Decimal] = mapped_column(Numeric(4, 2), default=0)
    frequencia_abs: Mapped[int] = mapped_column(Integer)
    frequencia_rel: Mapped[float] = mapped_column(Float) #Ver como vai funcionar
    aprovacao: Mapped[bool] = mapped_column(Boolean)

    # Ligações de ORM
    aluno: Mapped["Aluno"] = relationship(
        foreign_keys=[aluno_id],
        back_populates="matriculas"
    )

    turma: Mapped["Turma"] = relationship(
        foreign_keys=[turma_id],
        back_populates="matriculas"
    )

    disciplina: Mapped["Disciplina"] = relationship(
        foreign_keys=[disciplina_id],
    )

    # Constraints da tabela
    __table_args__ = ( # Nota == -1 -> Aluno faltou
        CheckConstraint("(nota1 = -1) OR (nota1 >= 0 AND nota1 <= 10)", name="ck_matricula_nota1"),
        CheckConstraint("(nota2 = -1) OR (nota2 >= 0 AND nota2 <= 10)", name="ck_matricula_nota2"),
        CheckConstraint("(nota3 = -1) OR (nota3 >= 0 AND nota3 <= 10)", name="ck_matricula_nota3"),
        CheckConstraint("(final = -1) OR (final >= 0 AND final <= 10)", name="ck_matricula_final"),
        CheckConstraint("media >= 0 AND media <= 10", name="ck_matricula_media"),
    )
