from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Time, ForeignKey
from sqlalchemy.orm import relationship

from ..db.database import db

class EventoRecorrente(db.Model):
    __tablename__ = "eventos_recorrentes"

    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    dia_semana = Column(Integer, nullable=False)  # 0 = segunda ... 6 = domingo
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)
    criado_por = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    criador = relationship("Usuario", back_populates="eventos_recorrentes")

    def __repr__(self) -> str:
        return f"<EventoRecorrente id={self.id} titulo={self.titulo}>"