# models.py - Modelos SQLAlchemy (mapeamento das tabelas)

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime,
    ForeignKey, Enum, Date, Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    foto_url = Column(String(255), default="/static/img/avatar_default.png")
    bio = Column(Text, nullable=True)
    is_admin = Column(Boolean, default=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    reviews = relationship("Review", back_populates="usuario", cascade="all, delete")
    favoritos = relationship("Favorito", back_populates="usuario", cascade="all, delete")
    status_jogos = relationship("StatusJogo", back_populates="usuario", cascade="all, delete")


class Jogo(Base):
    __tablename__ = "jogos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    desenvolvedora = Column(String(100), nullable=False)
    data_lancamento = Column(Date, nullable=True)
    descricao = Column(Text, nullable=True)
    lore = Column(Text, nullable=True)
    genero = Column(String(80), nullable=True)
    capa_url = Column(String(255), default="/static/img/capa_default.png")
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    reviews = relationship("Review", back_populates="jogo", cascade="all, delete")
    favoritos = relationship("Favorito", back_populates="jogo", cascade="all, delete")
    status_jogos = relationship("StatusJogo", back_populates="jogo", cascade="all, delete")

    @property
    def media_reviews(self):
        """Calcula média das notas das reviews."""
        if not self.reviews:
            return None
        return round(sum(r.nota for r in self.reviews) / len(self.reviews), 1)

    @property
    def total_reviews(self):
        return len(self.reviews)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    jogo_id = Column(Integer, ForeignKey("jogos.id"), nullable=False)
    nota = Column(Integer, nullable=False)  # 0-5
    comentario = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="reviews")
    jogo = relationship("Jogo", back_populates="reviews")


class Favorito(Base):
    __tablename__ = "favoritos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    jogo_id = Column(Integer, ForeignKey("jogos.id"), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", back_populates="favoritos")
    jogo = relationship("Jogo", back_populates="favoritos")


class StatusJogo(Base):
    __tablename__ = "status_jogo"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    jogo_id = Column(Integer, ForeignKey("jogos.id"), nullable=False)
    status = Column(Enum("jogando", "jogado", "quero_jogar"), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    usuario = relationship("Usuario", back_populates="status_jogos")
    jogo = relationship("Jogo", back_populates="status_jogos")
