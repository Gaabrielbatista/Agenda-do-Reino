from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, DateTime, Date, Time, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship

from ..db.database import db


class ExcecaoTipo(Enum):
    CANCELAMENTO = "cancelamento"
    REMARCACAO = "remarcacao"


class EventoExcecao(db.Model):
    """
    Representa uma exceção pontual para um EventoRecorrente.

    - CANCELAMENTO: a ocorrência de `data_original` está cancelada.
    - REMARCACAO:   a ocorrência de `data_original` foi movida para
                    `data_nova` / `hora_nova_inicio` / `hora_nova_fim`.
    """
    __tablename__ = "eventos_excecoes"

    id = Column(Integer, primary_key=True)

    # Qual regra recorrente está sendo excepcionada
    evento_recorrente_id = Column(
        Integer,
        ForeignKey("eventos_recorrentes.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Data da ocorrência original que está sendo alterada
    data_original = Column(
        DateTime,
        nullable=False,
        comment="Data/hora da ocorrência original que está sendo cancelada ou remarcada",
    )

    tipo = Column(SAEnum(ExcecaoTipo), nullable=False)

    # Campos preenchidos apenas para REMARCACAO
    data_nova = Column(DateTime, nullable=True)
    hora_nova_inicio = Column(Time, nullable=True)
    hora_nova_fim = Column(Time, nullable=True)

    motivo = Column(String, nullable=True)

    criado_por = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relacionamentos
    evento_recorrente = relationship("EventoRecorrente", back_populates="excecoes")
    criador = relationship("Usuario")

    def __repr__(self) -> str:
        return (
            f"<EventoExcecao id={self.id} "
            f"recorrente={self.evento_recorrente_id} "
            f"tipo={self.tipo.value} "
            f"data_original={self.data_original}>"
        )