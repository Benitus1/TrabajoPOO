# EcoTech Solutions - Sistema de Gestion (Unidad 3)

Proyecto en Python para la asignatura **Programacion Orientada a Objeto Seguro** (TI3021), correspondiente a la Evaluacion Formativa de la Unidad 3: **Consumo de Servicios Externos y Seguridad en Python**.

## Caracteristicas principales

### Gestion interna (ya existente)
- CRUD de empleados, departamentos, proyectos y registros de tiempo.
- Asignacion de empleados a departamentos y proyectos.
- Bitacora de horas por proyecto.
- Restauracion de la base de datos a estado base.

### Nuevas caracteristicas anadidas (Unidad 3)

#### 1. Consumo de servicios externos (APIs)
Menu: **Servicios Externos (API)** (opcion 6).

- **Clima por ciudad**: consulta el clima actual.
  - Si existe `OPENWEATHER_API_KEY` en el entorno, usa OpenWeatherMap.
  - Si no existe, usa Open-Meteo (sin clave) + geocodificacion.
- **Indicadores economicos**: consulta dolar, euro, UF, UTM y Bitcoin desde `mindicador.cl`.
- **Conversion de moneda**: convierte entre CLP, USD y EUR usando los indicadores anteriores.

Se utilizan solicitudes HTTP con la libreria oficial `requests` y procesamiento de respuestas JSON. Las claves de API se leen desde variables de entorno (`.env`), evitando su exposicion en el codigo.

#### 2. Seguridad: login y validacion de entradas
- **Login obligatorio** al iniciar la aplicacion.
- Contrasenas almacenadas como hash seguro (PBKDF2-HMAC-SHA256 con salt), nunca en texto plano.
- Control de acceso por roles: `Administrador`, `Gerente`, `Empleado`, `Lector`.
- **Validacion y saneamiento** de todas las entradas de usuario (nombres, emails, telefonos, fechas, salarios, ciudades, codigos, usuarios y contrasenas).
- Gestion de usuarios (solo administrador): crear, listar, eliminar y cambiar contrasena.

## Estructura del proyecto

```text
.
├── main.py
├── BASE/
│   └── ecotech.sql
├── DAO/
│   ├── conexion.py
│   ├── empleado_dao.py
│   ├── departamento_dao.py
│   ├── proyecto_dao.py
│   ├── proyecto_asignacion_dao.py
│   ├── registro_tiempo_dao.py
│   └── usuario_dao.py          # NUEVO
├── DTO/
│   ├── empleado_dto.py
│   ├── departamento_dto.py
│   ├── proyecto_dto.py
│   ├── registro_tiempo_dto.py
│   └── usuario_dto.py          # NUEVO
├── SEGURIDAD/                  # NUEVO
│   ├── __init__.py
│   ├── validaciones.py
│   └── autenticacion.py
├── SERVICIOS/                  # NUEVO
│   ├── __init__.py
│   ├── clima_service.py
│   └── indicadores_service.py
├── .env.example                # NUEVO
└── README.md