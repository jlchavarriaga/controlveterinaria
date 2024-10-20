## Grupo 1 - Gestion de Pacientes

### 1. Conexión a la base de datos
La función **get_db_connection()** establece una conexión con una base de datos que está en un servidor local. El código asume que el servidor está en el **puerto 3307** y que la base de datos es veterinaria. Usa la librería **pymysql**.

### 2. Clases con validación de datos (Modelos de Pydantic)
- Cliente: Define el modelo de cliente con atributos como nombre, teléfono, dirección, correo, y contacto de emergencia. Usa **Pydantic** para validaciones de los campos (longitud mínima/máxima, patrones de regex, etc.).

- Mascota: Similar al modelo Cliente, este define atributos como nombre, diagnóstico, peso, altura, fechas (nacimiento, ingreso, salida), tipo de sangre, y las relaciones con el cliente (cliente_id) y tipo de mascota (tipo_mascota_id).

- TipoMascota: Define el sexo, raza y tipo de animal (especie) de una mascota. Todos estos campos tienen validaciones.

### 3. Manejador de errores personalizados

```python
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errores = exc.errors()
    mensajes_error = []
    ...
    return JSONResponse(
        status_code=422,
        content={"detalle": mensajes_error}
    )
```

Esta sección intercepta errores de validación (como cuando los datos de una solicitud no cumplen con los requisitos de los modelos de Pydantic) y devuelve un mensaje personalizado al usuario.

### 4. Rutas (Endpoints)
- **Registrar Cliente:**
El endpoint /cliente/ permite registrar un nuevo cliente. Antes de insertar en la base de datos, se verifica si ya existe un cliente con el mismo teléfono o correo. Si existe, devuelve un error; si no, se inserta y se devuelve el ID generado.

- **Registrar Mascota:**
El endpoint /mascota/ inserta una nueva mascota. Verifica primero si ya existe una mascota con el mismo nombre asociada al mismo cliente. Si no existe, la inserta.

- **Registrar Tipo de Mascota:**
El endpoint /tipo_mascota/ permite registrar un nuevo tipo de mascota. Verifica primero si ya existe un tipo de mascota con la misma raza, sexo y especie, para evitar duplicados.
