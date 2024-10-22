from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    nombre_usuario: str
    email_usuario: str
    telefono_usuario: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id_usuario: int

    class Config:
        orm_mode = True

# Schemas para Animal, Cita, Tratamiento y Notificacion