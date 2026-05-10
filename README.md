# Roda Simulador de Crédito — Backend

API REST para simulación de crédito de movilidad eléctrica con Flask.

## Tecnologías

- Python 3.10+ / Flask 3.1
- Flask-SQLAlchemy 3.1 + PostgreSQL 14+
- Pydantic v2 para validación
- Decimal (Python) para precisión financiera

## Instalación

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuración

Copiar `.env.example` a `.env` y ajustar:

| Variable | Descripción | Default |
|---|---|---|
| `DATABASE_URL` | Conexión PostgreSQL | `postgresql://localhost:5432/roda` |
| `TASA_INTERES_ANUAL` | Tasa de interés anual (decimal) | `0.144` (14.4%) |
| `FLASK_ENV` | Entorno de ejecución | `development` |

## Ejecución

```bash
python app.py
```

El servidor inicia en `http://localhost:5000`. Las tablas se crean automáticamente al iniciar (`db.create_all()`).

## Endpoints

### POST /api/simulacion

Simula un crédito y devuelve el resumen con el plan de pagos.

```json
{
  "tipo_vehiculo": "bicicleta",
  "valor_vehiculo": 3500000,
  "cuota_inicial": 500000,
  "plazo_meses": 12
}
```

**Validaciones (400):**
- `tipo_vehiculo` debe ser `"bicicleta"` o `"moto"`
- `valor_vehiculo` >= 500000
- `cuota_inicial` >= 0 y menor a `valor_vehiculo`
- `plazo_meses` entre 1 y 60

**Respuesta 200:** `{ "id", "resumen", "plan_pagos" }`

### POST /api/solicitudes

Registra una solicitud asociada a una simulación existente.

```json
{
  "simulacion_id": 1,
  "nombre": "David",
  "apellido": "Daza",
  "email": "david@email.com",
  "telefono": "30282706085",
  "ciudad": "Bogotá"
}
```

**Validaciones (400):** nombre/apellido/ciudad requeridos, email con @ y ., teléfono solo dígitos.

**404:** si `simulacion_id` no existe.

**Respuesta 201:** `{ "id", "mensaje" }`

### GET /api/solicitudes/:id

Consulta una solicitud con los datos de su simulación asociada.

**404:** si la solicitud no existe.

**Respuesta 200:** `{ "id", "nombre", "apellido", "email", "telefono", "ciudad", "simulacion", "creado_en" }`

## Decisiones técnicas

- **Amortización francesa** con `Decimal` y redondeo `ROUND_HALF_UP`. Sin errores de punto flotante.
- **El plan de pagos no se persiste.** Se calcula en memoria (O(n), n ≤ 60). En producción se agregaría una tabla `cuotas`.
- **Sin migraciones.** `db.create_all()` es suficiente para el alcance de la prueba.
- **Sin autenticación.** Los endpoints son públicos.
- **Tasa configurable** por variable de entorno. Default 14.4% anual, realista para Colombia.
- **CORS** con `origins: "*"` para desarrollo.
