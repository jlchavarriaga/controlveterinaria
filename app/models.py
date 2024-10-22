#app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String, index=True)
    email_usuario = Column(String, unique=True, index=True)
    telefono_usuario = Column(String)

    animales = relationship("Animal", back_populates="usuario")

class Animal(Base):
    __tablename__ = "animales"
    id_animal = Column(Integer, primary_key=True, index=True)
    nombre_animal = Column(String)
    tipo_animal = Column(String)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))

    usuario = relationship("Usuario", back_populates="animales")

class Cita(Base):
    __tablename__ = "citas"
    id_cita = Column(Integer, primary_key=True, index=True)
    fecha_cita = Column(DateTime)
    id_animal = Column(Integer, ForeignKey("animales.id_animal"))

class Tratamiento(Base):
    __tablename__ = "tratamientos"
    id_tratamiento = Column(Integer, primary_key=True, index=True)
    nombre_tratamiento = Column(String)
    descripcion_tratamiento = Column(String)
    id_animal = Column(Integer, ForeignKey("animales.id_animal"))

class Notificacion(Base):
    __tablename__ = "notificaciones"
    id_notificaciones = Column(Integer, primary_key=True, index=True)
    fecha_envio_notificaciones = Column(DateTime)
    mensaje_notificaciones = Column(String)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_animal = Column(Integer, ForeignKey("animales.id_animal"))
    id_tratamiento = Column(Integer, ForeignKey("tratamientos.id_tratamiento"))