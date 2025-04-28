
# Proyecto: prueba_alfred

Bienvenido al repositorio de prueba_alfred, un proyecto que te permitirá gestionar viajes de usuarios y conductores de forma sencilla y eficiente. Sigue los pasos a continuación para configurar el entorno y comenzar a trabajar con la API.

## 🚀 Pasos para comenzar

### 1. Clonar el repositorio

Primero, clona este repositorio a tu máquina local:

```bash
git clone <url_del_repositorio>
```

### 2. Configuración del archivo `.env`

Crea un archivo `.env` en el directorio raíz del proyecto. Puedes copiar el archivo `.env.example` y realizar las siguientes modificaciones:

- **`DATABASE_HOST`**: Cambia el valor de `"localhost"` a `"db"`.
- **`MAPBOX_API_KEY`**: Sustituye `"example"` por la clave de API que recibirás por correo.

### 3. Correr las migraciones

Para correr las migraciones de la base de datos, utiliza Docker y sigue estos pasos:

```bash
docker exec -it prueba_alfred-web-1 bash
```

Una vez dentro del contenedor, ejecuta:

```bash
python manage.py migrate
```

Esto configurará la base de datos y te permitirá comenzar con la aplicación.

### 4. Ejecutar la aplicación

Con las migraciones completadas, deberías tener la aplicación corriendo en el puerto **8000**. Accede a ella en:

```
http://localhost:8000/
```

## 🔥 Rutas y herramientas disponibles

### 1. **Rutas Swagger**

Para explorar las rutas disponibles de la API, puedes acceder a:

```
http://localhost:8000/swagger/
```

### 2. **Postman Collection**

Si prefieres usar Postman, puedes revisar y probar las rutas utilizando esta colección compartida:

[Postman Collection](https://winter-water-758647.postman.co/workspace/Personal-Workspace~71a70eaa-182c-432c-b9b4-2dfdeafb1a62/collection/30261599-f7991a7c-3d84-42c7-9282-b093d7aa1566?action=share&creator=30261599)

### 3. **Autorización**

Para autenticarte en la API, utiliza el siguiente encabezado en las solicitudes:

- **Key**: `Authorization`
- **Value**: `Token <tuToken>`

---

## 👤 Descripción del uso por tipo de usuario

### Para usuarios normales

1. **Registrarse como usuario**:

   ```http
   POST http://localhost:8000/api/users/register/
   ```

2. **Iniciar sesión y obtener el token**:

   ```http
   POST http://127.0.0.1:8000/api/users/login/
   ```

3. **Crear un viaje** (Recibirás detalles del viaje y el conductor):

   ```http
   POST http://127.0.0.1:8000/api/trips/trips/create/
   ```

---

### Para conductores de la app

1. **Registrarse como conductor**:

   ```http
   POST http://localhost:8000/api/users/register/
   ```

2. **Iniciar sesión y obtener el token**:

   ```http
   POST http://127.0.0.1:8000/api/users/login/
   ```

3. **Crear un conductor**:

   ```http
   POST http://127.0.0.1:8000/api/drivers/drivers/create/
   ```

   - Si eres el conductor más cercano al usuario que ha creado un viaje, serás asignado automáticamente.

4. **Actualizar el estado del viaje** (cuando el viaje termine):

   ```http
   PUT http://127.0.0.1:8000/api/trips/trips/driver/<DriverId>/status/
   ```

---

## ☁️ Recomendación para despliegue en la nube

Para facilitar la gestión de tu aplicación y base de datos, te recomiendo usar los siguientes servicios de Amazon:

- **Amazon ECS**: Gestiona automáticamente los contenedores de tu aplicación, escalándolos según el tráfico.
- **Amazon RDS**: Mantiene tu base de datos segura, actualizada y disponible sin complicaciones.

Estos servicios permiten centrarte en el desarrollo, sin preocuparte por la infraestructura.

---

¡Y eso es todo! Ahora estás listo para comenzar a trabajar con prueba_alfred. Si tienes alguna pregunta o problema, no dudes en abrir un **issue** en este repositorio.

--- 

¡Diviértete programando! 🚀
