# Dockerfile
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar todos los archivos de la aplicación al contenedor
COPY ./app /app/app
COPY ./app/requirements.txt /app/requirements.txt

# Actualizar pip a la última versión
RUN pip install --upgrade pip


# Instalar las dependencias
RUN pip install --no-cache-dir -r /app/requirements.txt

# Ejecutar la aplicación con uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
