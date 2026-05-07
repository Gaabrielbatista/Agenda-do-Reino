from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship

from ..db.database import db

class EventoStatus(Enum):
    ATIVO = "ativo"
    CANCELADO = "cancelado"

class EventoNormal(db.Model):
    __tablename__ = "eventos_normais"

    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=True)
    status = Column(SAEnum(EventoStatus), nullable=False, default=EventoStatus.ATIVO)
    criado_por = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    criador = relationship("Usuario", back_populates="eventos_normais")

    def __repr__(self) -> str:
        return f"<EventoNormal id={self.id} titulo={self.titulo}>"
