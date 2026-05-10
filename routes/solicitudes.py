from flask import Blueprint, jsonify, request
from pydantic import BaseModel, ValidationError, field_validator

from models import Simulacion, Solicitud, db

solicitudes_bp = Blueprint("solicitudes", __name__)


class SolicitudRequest(BaseModel):
    simulacion_id: int
    nombre: str
    apellido: str
    email: str
    telefono: str
    ciudad: str

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v):
        if not v.strip():
            raise ValueError("nombre es obligatorio")
        return v.strip()

    @field_validator("apellido")
    @classmethod
    def validar_apellido(cls, v):
        if not v.strip():
            raise ValueError("apellido es obligatorio")
        return v.strip()

    @field_validator("email")
    @classmethod
    def validar_email(cls, v):
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("email no tiene un formato valido")
        return v.strip()

    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, v):
        if not v.isdigit():
            raise ValueError("telefono debe contener solo numeros")
        return v.strip()

    @field_validator("ciudad")
    @classmethod
    def validar_ciudad(cls, v):
        if not v.strip():
            raise ValueError("ciudad es obligatorio")
        return v.strip()


@solicitudes_bp.route("/api/solicitudes", methods=["POST"])
def registrar():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "El cuerpo de la peticion debe ser JSON"}), 400

    try:
        req = SolicitudRequest.model_validate(data)
    except ValidationError as e:
        primer_error = e.errors()[0]["msg"]
        return jsonify({"error": primer_error}), 400

    simulacion = db.session.get(Simulacion, req.simulacion_id)
    if simulacion is None:
        return (
            jsonify(
                {"error": f"La simulacion con id {req.simulacion_id} no existe"}
            ),
            404,
        )

    solicitud = Solicitud(
        simulacion_id=req.simulacion_id,
        nombre=req.nombre,
        apellido=req.apellido,
        email=req.email,
        telefono=req.telefono,
        ciudad=req.ciudad,
    )
    db.session.add(solicitud)
    db.session.commit()

    return (
        jsonify(
            {"id": solicitud.id, "mensaje": "Solicitud registrada exitosamente"}
        ),
        201,
    )


@solicitudes_bp.route("/api/solicitudes/<int:solicitud_id>", methods=["GET"])
def consultar(solicitud_id):
    solicitud = db.session.get(Solicitud, solicitud_id)
    if solicitud is None:
        return jsonify({"error": "Solicitud no encontrada"}), 404

    return jsonify(
        {
            "id": solicitud.id,
            "nombre": solicitud.nombre,
            "apellido": solicitud.apellido,
            "email": solicitud.email,
            "telefono": solicitud.telefono,
            "ciudad": solicitud.ciudad,
            "simulacion": {
                "tipo_vehiculo": solicitud.simulacion.tipo_vehiculo,
                "valor_vehiculo": float(solicitud.simulacion.valor_vehiculo),
                "cuota_mensual": float(solicitud.simulacion.cuota_mensual),
                "plazo_meses": solicitud.simulacion.plazo_meses,
            },
            "creado_en": solicitud.creado_en.isoformat(),
        }
    ), 200
