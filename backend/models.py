from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    equipos = relationship("EquipoUsuario", back_populates="usuario")

class Liga(Base):
    __tablename__ = "ligas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    provider = Column(String, nullable=False)  # ej: "laliga_fantasy"
    external_id = Column(String, unique=True)

    equipos = relationship("EquipoUsuario", back_populates="liga")

class Jugador(Base):
    __tablename__ = "jugadores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    posicion = Column(String, nullable=False)   # ej: "DEL", "DEF", "POR", "CEN"
    equipo_real = Column(String, nullable=False)
    provider_id = Column(String, unique=True)

    plantillas = relationship("Plantilla", back_populates="jugador")
    precios = relationship("PrecioHistorico", back_populates="jugador")
    puntos = relationship("PuntosHistorico", back_populates="jugador")

class EquipoUsuario(Base):
    __tablename__ = "equipos_usuario"
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"))
    id_liga = Column(Integer, ForeignKey("ligas.id"))
    saldo = Column(Float, default=0.0)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("User", back_populates="equipos")
    liga = relationship("Liga", back_populates="equipos")
    plantilla = relationship("Plantilla", back_populates="equipo")

class Plantilla(Base):
    __tablename__ = "plantillas"
    id = Column(Integer, primary_key=True, index=True)
    id_equipo = Column(Integer, ForeignKey("equipos_usuario.id"))
    id_jugador = Column(Integer, ForeignKey("jugadores.id"))
    precio_compra = Column(Float)
    fecha_alta = Column(DateTime, default=datetime.utcnow)
    estado = Column(String, default="activo")  # "activo", "vendido"

    equipo = relationship("EquipoUsuario", back_populates="plantilla")
    jugador = relationship("Jugador", back_populates="plantillas")

class Mercado(Base):
    __tablename__ = "mercado"
    id = Column(Integer, primary_key=True, index=True)
    id_liga = Column(Integer, ForeignKey("ligas.id"))
    id_jugador = Column(Integer, ForeignKey("jugadores.id"))
    precio_salida = Column(Float)
    vendedor = Column(String)
    fecha_publicacion = Column(DateTime, default=datetime.utcnow)
    fecha_cierre = Column(DateTime)

class PrecioHistorico(Base):
    __tablename__ = "precios_historicos"
    id = Column(Integer, primary_key=True, index=True)
    id_jugador = Column(Integer, ForeignKey("jugadores.id"))
    fecha = Column(DateTime, default=datetime.utcnow)
    precio = Column(Float, nullable=False)

    jugador = relationship("Jugador", back_populates="precios")

class PuntosHistorico(Base):
    __tablename__ = "puntos_historicos"
    id = Column(Integer, primary_key=True, index=True)
    id_jugador = Column(Integer, ForeignKey("jugadores.id"))
    jornada = Column(Integer, nullable=False)
    puntos = Column(Float, nullable=False)

    jugador = relationship("Jugador", back_populates="puntos")