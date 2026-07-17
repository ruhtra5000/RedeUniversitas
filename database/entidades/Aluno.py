from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base

if TYPE_CHECKING:
    from database.entidades.Bolsa import Bolsa
    from database.entidades.Campus import Campus
    from database.entidades.Curso import Curso
    from database.entidades.Matricula import Matricula
    from database.entidades.Mensalidade import Mensalidade
    from database.entidades.Pessoa import Pessoa

class Aluno(Base):
    __tablename__ = "aluno"

    # Colunas
    pessoa_id: Mapped[int] = mapped_column(Integer, ForeignKey("pessoa.id"), primary_key=True)
    matricula: Mapped[str] = mapped_column(String(25), nullable=False)
    media_geral: Mapped[float] = mapped_column(Float, default=0.0)
    coef_rend: Mapped[float] = mapped_column(Float, default=0.0)
    campus_id: Mapped[int] = mapped_column(ForeignKey("campus.id"))
    curso_id: Mapped[int] = mapped_column(ForeignKey("curso.id"))

    # Ligações de ORM
    pessoa: Mapped["Pessoa"] = relationship(
        back_populates="aluno",
        uselist=False
    )

    campus: Mapped["Campus"] = relationship(
        foreign_keys=[campus_id]
    )

    curso: Mapped["Curso"] = relationship(
        foreign_keys=[curso_id]
    )

    matriculas: Mapped[list["Matricula"]] = relationship(
        foreign_keys="Matricula.aluno_id",
        back_populates="aluno"
    )

    bolsas: Mapped[list["Bolsa"]] = relationship(
        foreign_keys="Bolsa.aluno_id",
        back_populates="aluno"
    )

    mensalidades: Mapped[list["Mensalidade"]] = relationship(
        foreign_keys="Mensalidade.aluno_id",
        back_populates="aluno"
    )

    # Constraints da tabela
    __table_args__ = (
        CheckConstraint(
            "media_geral >= 0 AND media_geral <= 10",
            name="ck_aluno_media_geral"
        ),
        CheckConstraint(
            "coef_rend >= 0 AND coef_rend <= 10", 
            name="ck_aluno_coef_rend"
        ),
        UniqueConstraint( # Alunos devem ter uma matrícula única por campus
            "campus_id",
            "matricula",
            name="uq_aluno_campus_matricula"
        ),
    )