# API de Reservas - Club Deportivo Encuentro

Backend desarrollado en Python y Flask para la gestión de canchas, socios, disponibilidades y reservas del Club Deportivo Encuentro.

## Integrantes
* **Facundo Frisa** - 116621 / 47205331
* **Matías Alejandro Ozores** - 116166 / 47760583
* **Ivan Ruddy Aracena Choque** - 115221 / 96165428
* **Nicolás Valenzuela** - 106191 / 40242029

## Tecnologías y Versiones Utilizadas
* **Lenguaje:** Python 3.12+
* **Framework Web:** Flask 3.0+
* **Base de Datos:** MySQL 8.0+ (Engine InnoDB, charset `utf8mb4`)
* **Conector BD:** PyMySQL 1.1+
* **Gestión de Entorno:** python-dotenv 1.0+
* **Testing:** pytest 9.1+

## Configuración del Entorno
El proyecto utiliza variables de entorno para mantener separada la configuración del código fuente y evitar la exposición de credenciales en el repositorio.

1. Crear el archivo `.env` tomando como base la plantilla `.env.example`:
   ```bash
   cp .env.example .env
   ```
2. Ajustar los parámetros según la configuración local de MySQL (por ejemplo, XAMPP):
   ```env
   FLASK_ENV=development
   PORT=5000
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=tu_contraseña
   DB_NAME=club_deportivo
   ```

## Pasos de Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/matiasozores/ids-reservas-club-deportivo.git
cd ids-reservas-club-deportivo
```

### 2. Crear y activar el entorno virtual
* **Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
* **Windows (Git Bash / MINGW64):**
  ```bash
  python -m venv venv
  source venv/Scripts/activate
  ```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Inicializar la Base de Datos
Asegurarse de tener el servidor MySQL iniciado y ejecutar el script de inicialización `init_db.sql` para crear el esquema y precargar los deportes obligatorios:
```bash
mysql -u root -p < scripts/init_db.sql
```

### 5. Ejecutar la aplicación
```bash
python app.py
```
La API quedará escuchando en `http://localhost:5000` (o el puerto configurado en el `.env`).

---

## Ejemplos de Solicitudes (API Requests)

### 1. Prueba de vida (Health Check)
* **GET** `/health`
* **Respuesta (`200 OK`):**
  ```json
  {
    "status": "ok",
    "message": "API Club Deportivo funcionando correctamente"
  }
  ```

### 2. Consultar deportes precargados
* **GET** `/deportes`
* **Respuesta (`200 OK`):**
  ```json
  {
    "deportes": [
      { "id": 1, "nombre": "Fútbol" },
      { "id": 2, "nombre": "Tenis" },
      { "id": 3, "nombre": "Pádel" }
    ]
  }
  ```

### 3. Registrar un socio
* **POST** `/socios`
* **Cuerpo de la solicitud (`application/json`):**
  ```json
  {
    "nombre": "Juan Pérez",
    "email": "juan.perez@email.com"
  }
  ```
* **Respuesta (`201 Created`):** Crea el primer socio necesario para realizar la reserva (id_socio: 1).
* **Cuerpo de la respuesta (`application/json`):**
  ```json
  {
    "id": 1, 
    "nombre": "Juan Pérez", 
    "email": "juan.perez@email.com", 
    "activo": true
  }
  ```

### 4. Registrar una cancha 
* **POST** `/canchas`
* **Cuerpo de la solicitud (`application/json`):**
  ```json
  {
    "nombre": "Cancha 1 - Fútbol 5", 
    "id_deporte": 1, 
    "precio_hora": 1500000
  }
  ```
* **Respuesta (`201 Created`):** Crea la primera cancha asociada al deporte Futbol.
* **Cuerpo de la respuesta (`application/json`):**
  ```json
  {
    "id": 1, 
    "nombre": "Cancha 1 - Fútbol 5", 
    "id_deporte": 1, 
    "precio_hora": 1500000, 
    "techada": false,
    "activa": true
  }
  ```

### 5. Consultar disponibilidad de canchas
* **GET** `/canchas/disponibles?fecha=2026-10-15&hora_inicio=18:00:00&hora_fin=20:00:00`
* **Respuesta (`200 OK`):**
* **Cuerpo de la respuesta (`application/json`):**
  ```json
  {
  "canchas": [
    {
      "id": 1,
      "nombre": "Cancha 1 - Fútbol 5",
      "id_deporte": 1,
      "precio_hora": 1500000,
      "techada": false,
      "activa": true
    }
  ],
  "_links": {
    "_first": {
      "href": "http://127.0.0.1:5000/canchas/disponibles?_limit=10&_offset=0&fecha=2026-10-15&hora_inicio=18:00:00&hora_fin=20:00:00"
    },
    "_last": {
      "href": "http://127.0.0.1:5000/canchas/disponibles?_limit=10&_offset=0&fecha=2026-10-15&hora_inicio=18:00:00&hora_fin=20:00:00"
    }
  }
  }
  ```
### 6. Crear una reserva
* **POST** `/reservas`
* **Cuerpo de la solicitud (`application/json`):**
  ```json
  {
    "id_socio": 1, 
    "id_cancha": 1, 
    "fecha_hora_inicio": "2026-10-15T18:00:00.000000-03:00", 
    "fecha_hora_fin": "2026-10-15T20:00:00.000000-03:00"
  }
  ```
* **Respuesta (`201 Created`):**
* **Cuerpo de la respuesta (`application/json`):**
  ```json
  {
    "id": 1,
    "id_socio": 1,
    "id_cancha": 1,
    "fecha_hora_inicio": "2026-10-15T18:00:00.000000-03:00",
    "fecha_hora_fin": "2026-10-15T20:00:00.000000-03:00",
    "estado": "confirmada",
    "precio_hora": 1500000,
    "precio_total": 3000000
  }
  ```
---

## Supuestos Adoptados y Reglas de Negocio

* **Alcance del proyecto:** Administración exclusiva de un único club deportivo. No se gestionan pagos, cuotas sociales, torneos ni inscripciones a clases.
* **Horarios de atención:** El club opera todos los días de 08:00 a 23:00 hs sin excepción por feriados.
* **Duración e intervalos:** Las reservas duran entre 1 y 3 horas completas, inician y finalizan en horas en punto y no pueden atravesar la medianoche.
* **Zona Horaria y Formato:** Todas las fechas y horas se manejan en formato ISO 8601 con desplazamiento fijo GMT-3 (`YYYY-MM-DDTHH:MM:SS.ffffff-03:00`).
* **Manejo de importes:** Todos los precios y tarifas se expresan en enteros como cantidad de centavos (ejemplo: `$10.000,00` equivale a `1000000` centavos).
* **Superposiciones:** Se rechazan reservas que presenten superposición horaria tanto para la misma cancha como para el mismo socio.
* **Conservación de tarifas:** Al crear la reserva se congela la tarifa por hora vigente y el total; posteriores cambios en el precio de la cancha no modifican reservas previas.
