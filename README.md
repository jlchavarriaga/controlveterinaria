# controlveterinaria
Objetivo academico

# Clonar el repositorio
git clone https://github.com/jlchavarriaga/controlveterinaria
cd controlveterinaria

# Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows
venv\Scripts\activate
# En macOS/Linux
# source venv/bin/activate

# Instalar las dependencias
pip install -r requirements.txt

# Configurar el archivo .env con las variables de entorno necesarias (e.g., SECRET_KEY, DATABASE_URL, etc.)

# Iniciar la aplicación con Docker
docker-compose up --build

# Acceder a la aplicación
# Abre en tu navegador: http://localhost:8000
# Acceder a la documentación interactiva de la API: http://localhost:8000/docs

# Para actualizar el archivo de dependencias si añades nuevas librerías:
pip freeze > requirements.txt

# Asegúrate de tener la última versión de pip antes de instalar dependencias
python.exe -m pip install --upgrade pip
