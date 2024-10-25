from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.schemas import UserCreate, RoleCreate, User, Role
from app.crud import create_user, create_role
from app.models import User, Role
from app.routers import pacientes  # Importa correctamente el router de pacientes

app = FastAPI()

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello, World"}

# Dependencia para la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/roles/", response_model=Role)
def create_role_endpoint(role: RoleCreate, db: Session = Depends(get_db)):
    return create_role(db, role)

@app.post("/users/", response_model=User)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

# Incluir el router de pacientes
app.include_router(pacientes.router)
