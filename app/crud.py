# app/crud.py
from sqlalchemy.orm import Session
from app.models import Usuario, Animal
from app.schemas import CrearUsuario, animales
from app.auth import get_password_hash

def create_role(db: Session, role: animales):
    db_role = Animal(name=role.name, description=role.description)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def create_user(db: Session, user: CrearUsuario):
    hashed_password = get_password_hash(user.password)
    db_user = Usuario(username=user.username, hashed_password=hashed_password, role_id=user.role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.username == username).first()
from sqlalchemy.orm import Session
from . import models, schemas

# CRUD de usuario
def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def get_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

# Puedes agregar funciones similares para Cita, Tratamiento y Notificaciones
