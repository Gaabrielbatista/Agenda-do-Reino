from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship

from ..db.database import db

class UserType(Enum):
    ADMIN = "admin"
    MEMBRO = "membro"

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
