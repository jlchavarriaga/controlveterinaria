from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, crud, schemas
from .database import SessionLocal, engine, init_db

app = FastAPI()

@app.get('')
async def read_root():
    return{"Sistema de notificaciones, recibiras tu fokin notificaciones!"}

#Iniciar la base de datos
init_db()

# Dependencia de la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/usuarios/", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db=db, usuario=usuario)

# Endpoint para notificaciones
@app.post("/notificaciones/")
def programar_notificacion(id_usuario: int, mensaje: str, via: str, db: Session = Depends(get_db)):
    usuario = crud.get_usuario(db, id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if via == "sms":
        send_sms(usuario.telefono_usuario, mensaje)
    elif via == "whatsapp":
        send_whatsapp(usuario.telefono_usuario, mensaje)
    elif via == "email":
        send_email(usuario.email_usuario, "Recordatorio", mensaje)

    return {"mensaje": "Notificación programada"}