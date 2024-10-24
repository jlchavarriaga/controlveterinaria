from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, crud, schemas  
from app.database import SessionLocal, engine, init_db  
from app.notifications import send_sms, send_whatsapp_notification, send_email  

app = FastAPI()

# Iniciar la base de datos
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
        send_whatsapp_notification(usuario.telefono_usuario, mensaje)
    elif via == "email":
        send_email(usuario.email_usuario, "Recordatorio", mensaje)

    return {"mensaje": "Notificación programada"}
@app.post("/send-whatsapp/")
def send_notification(phone: str, date: str, time: str):
    """
    Endpoint para enviar notificaciones de WhatsApp.
    Args:
        phone (str): Número de teléfono destino en formato E.164.
        date (str): Fecha de la cita (fecha: "24/10/2024").
        time (str): Hora de la cita (hora: "9:30am").
    """
    send_whatsapp_notification(phone, date, time)
    return {"status": "Notificación enviada por WhatsApp"}