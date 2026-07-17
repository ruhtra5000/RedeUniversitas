from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date, Enum, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base
from database.entidades.enums.StatusBolsa import StatusBolsa

if TYPE_CHECKING:
    from database.entidades.Aluno import Aluno

class Bolsa(Base):
    __tablename__ = "bolsa"

    # Colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    aluno_id: Mapped[int] = mapped_column(ForeignKey("aluno.pessoa_id"))
    tipo_bolsa: Mapped[str] = mapped_column(String(25), nullable=False)
    percentual_desconto: Mapped[float] = mapped_column(Float, nullable=False) # Faixa: [0, 1]
    data_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    data_fim: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped["StatusBolsa"] = mapped_column(Enum(StatusBolsa), nullable=False)

    # Ligações de ORM
    aluno: Mapped["Aluno"] = relationship(
        foreign_keys=[aluno_id],
        back_populates="bolsas"
    )

    # Constraints da tabela
    __table_args__ = (
        # Cada aluno só pode ter uma única bolsa 
        # com status ATIVA vinculada a ele
        Index( 
            "uq_bolsa_ativa",
            "aluno_id",
            unique=True,
            postgresql_where=(status == StatusBolsa.ATIVA)
        ),
        CheckConstraint(
            "percentual_desconto >= 0 AND percentual_desconto <= 1", 
            name="ck_bolsa_percentual_desconto"
        ),
    )