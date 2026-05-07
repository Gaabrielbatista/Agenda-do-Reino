from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum, Boolean, Time, ForeignKey
from sqlalchemy.orm import relationship

from ..db.database import db

class UserType(Enum):
    ADMIN = "admin"
    MEMBRO = "membro"

class EventoStatus(Enum):
    ATIVO = "ativo"
    CANCELADO = "cancelado"

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    tipo = Column(SAEnum(UserType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    eventos_normais = relationship("EventoNormal", back_populates="criador", cascade="all, delete-orphan")
    eventos_recorrentes = relationship("EventoRecorrente", back_populates="criador", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Usuario id={self.id} email={self.email}>"
    
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
