# app/main.py
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import pymysql


def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='veterinaria',
        port=3307
    )

app = FastAPI()

# Validaciones para la clase Cliente
class Cliente(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    telefono: str = Field(..., pattern=r'^\d{10}$', description="Debe ser un número de teléfono de 10 dígitos")
    direccion: str = Field(..., min_length=5, max_length=150)
    correo: str = Field(..., min_length=5, max_length=100, description="Correo electrónico")
    contacto_emergencia: str = Field(..., min_length=10, max_length=100)

# Validaciones para la clase Mascota
class Mascota(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50, description="El nombre de la mascota debe tener entre 2 y 50 caracteres")
    nombre_cliente: str = Field(..., min_length=2, max_length=100, description="El nombre del dueño debe tener entre 2 y 100 caracteres")
    fecha_nacimiento: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$', description="La fecha de nacimiento debe tener el formato YYYY-MM-DD")    
    diagnostico: str = Field(..., min_length=5, max_length=200, description="El diagnóstico debe tener entre 5 y 200 caracteres")
    peso: float = Field(..., gt=0, description="El peso debe ser mayor a 0")
    altura: float = Field(..., gt=0, description="La altura debe ser mayor a 0")
    fecha_ingreso: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$', description="La fecha de ingreso debe tener el formato YYYY-MM-DD")   
    fecha_salida: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$', description="La fecha de salida debe tener el formato YYYY-MM-DD")
    tipo_sangre: str = Field(..., min_length=1, max_length=3, description="El tipo de sangre debe tener entre 1 y 3 caracteres")
    carnet_vacunas: bool = Field(..., description="Debe indicar si la mascota tiene carnet de vacunas")
    cliente_id: int = Field(..., gt=0, description="El ID del dueño debe ser mayor que 0")
    tipo_mascota_id: int = Field(..., gt=0, description="El ID del tipo de mascota debe ser mayor que 0")

# Validaciones para la clase TipoMascota
class TipoMascota(BaseModel):
    sexo: str = Field(..., pattern=r'^(Macho|Hembra)$', description="El sexo debe ser 'Macho' o 'Hembra'")
    raza: str = Field(..., min_length=3, max_length=50, description="La raza debe tener entre 3 y 50 caracteres")
    tipo_animal: str = Field(..., min_length=3, max_length=50, description="El tipo de animal debe tener entre 3 y 50 caracteres")
# Manejador de errores personalizados
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errores = exc.errors()
    mensajes_error = []
    
    for error in errores:
        campo = error["loc"][-1]  # Última ubicación, es decir, el campo con error
        mensaje = error["msg"]

        # Mensajes personalizados en español
        if "min_length" in mensaje:
            mensajes_error.append(f"El campo '{campo}' es demasiado corto. Verifica que tenga la longitud mínima requerida.")
        elif "max_length" in mensaje:
            mensajes_error.append(f"El campo '{campo}' es demasiado largo. Verifica que no exceda la longitud máxima permitida.")
        elif "pattern" in mensaje:
            if campo == "telefono":
                mensajes_error.append(f"El campo '{campo}' debe ser un número de teléfono válido de 10 dígitos.")
            else:
                mensajes_error.append(f"El campo '{campo}' tiene un formato incorrecto. Verifica el formato adecuado.")
        elif "regex" in mensaje:
            mensajes_error.append(f"El campo '{campo}' no coincide con el formato requerido. Verifica que sea correcto.")
        elif "gt" in mensaje:  
            mensajes_error.append(f"El valor de '{campo}' debe ser mayor que 0.")
        else:
            mensajes_error.append(f"Error en el campo '{campo}': {mensaje}")

    return JSONResponse(
        status_code=422,
        content={"detalle": mensajes_error}
    )

@app.post("/cliente/")
async def registrar_cliente(cliente: Cliente):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        # Verifica si ya existe un cliente con el mismo teléfono o correo
        query_check = "SELECT COUNT(*) FROM cliente WHERE telefono = %s OR correo = %s"
        cursor.execute(query_check, (cliente.telefono, cliente.correo))
        count = cursor.fetchone()[0]

        if count > 0:
            return JSONResponse(status_code=400, content={"detail": "Ya existe un cliente con ese teléfono o correo."})

        # Inserta el nuevo cliente
        query = "INSERT INTO cliente(nombre, telefono, direccion, correo, contacto_emergencia) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(query, (cliente.nombre, cliente.telefono, cliente.direccion, cliente.correo, cliente.contacto_emergencia))
        db.commit()
        cliente_id = cursor.lastrowid  # Obtener el ID del cliente recién registrado

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
    finally:
        cursor.close()
        db.close()

    # Genera el endpoint del usuario basado en el ID del cliente
    usuario_endpoint = f"/usuarios/{cliente_id}"

    # Devuelve el ID del cliente, el mensaje de éxito y el endpoint de usuario
    return {"message": "Dueño registrado exitosamente", "cliente_id": cliente_id, "usuario_endpoint": usuario_endpoint}
@app.post("/mascota/")
async def registrar_mascota(mascota: Mascota):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        # Verifica si ya existe una mascota con el mismo nombre para el mismo cliente
        query_check = "SELECT COUNT(*) FROM mascota WHERE nombre = %s AND cliente_id = %s"
        cursor.execute(query_check, (mascota.nombre, mascota.cliente_id))
        count = cursor.fetchone()[0]

        if count > 0:
            return JSONResponse(status_code=400, content={"detail": "Ya existe una mascota con ese nombre para este cliente."})

        # Inserta la nueva mascota
        query = """
        INSERT INTO mascota(nombre, fecha_nacimiento, diagnostico, peso, altura, fecha_ingreso, fecha_salida, tipo_sangre, carnet_vacunas, cliente_id, tipo_mascota_id) 
        VALUES (%s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (mascota.nombre, mascota.fecha_nacimiento, mascota.diagnostico, mascota.peso, mascota.altura, mascota.fecha_ingreso, mascota.fecha_salida, mascota.tipo_sangre, mascota.carnet_vacunas, mascota.cliente_id, mascota.tipo_mascota_id))
        db.commit()
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
    finally:
        cursor.close()
        db.close()

    return {"message": "Mascota registrada exitosamente"}


@app.post("/tipo_mascota/")
async def registrar_tipo_mascota(tipo: TipoMascota):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        # Verifica si ya existe el tipo de mascota
        query_check = "SELECT COUNT(*) FROM tipo_mascota WHERE sexo = %s AND raza = %s AND tipo_animal = %s"
        cursor.execute(query_check, (tipo.sexo, tipo.raza, tipo.tipo_animal))
        count = cursor.fetchone()[0]

        if count > 0:
            return JSONResponse(status_code=400, content={"detail": "El tipo de mascota ya existe."})

        # Inserta el nuevo tipo de mascota
        query = "INSERT INTO tipo_mascota(sexo, raza, tipo_animal) VALUES (%s, %s, %s)"
        cursor.execute(query, (tipo.sexo, tipo.raza, tipo.tipo_animal))
        db.commit()
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
    finally:
        cursor.close()
        db.close()
    
    return {"message": "Tipo de mascota registrado exitosamente"}
