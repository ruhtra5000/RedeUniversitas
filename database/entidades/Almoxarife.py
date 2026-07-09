from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Base import Base

if TYPE_CHECKING:
    from database.entidades.Pessoa import Pessoa

class Almoxarife(Base):
    __tablename__ = "almoxarife"

    # Colunas
    pessoa_id: Mapped[int] = mapped_column(ForeignKey("pessoa.id"), primary_key=True)

    # Ligações de ORM
    pessoa: Mapped["Pessoa"] = relationship(
        back_populates="almoxarife"
    )