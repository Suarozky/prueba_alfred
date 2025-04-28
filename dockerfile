
FROM python:3.11-slim

# Definir el directorio de trabajo
WORKDIR /app

# Copiar los archivos de tu proyecto a /app
COPY . /app/

# Instalar las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que Django usa por defecto
EXPOSE 8000

# Comando para correr el servidor Django
# Otros pasos en tu Dockerfile
# Copia tus archivos de aplicación y dependencias
COPY . /app/

# Instalar dependencias
RUN pip install -r /app/requirements.txt

# Ejecutar las migraciones y luego el servidor
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

