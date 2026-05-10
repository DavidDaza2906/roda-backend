from decimal import Decimal

from flask import Blueprint, jsonify, request
from pydantic import BaseModel, ValidationError, field_validator, model_validator

from amortizacion import calcular_amortizacion
from config import Config
from models import Simulacion, db

simulacion_bp = Blueprint("simulacion", __name__)


class SimulacionRequest(BaseModel):
    tipo_vehiculo: str
    valor_vehiculo: Decimal
    cuota_inicial: Decimal
    plazo_meses: int

    @field_validator("tipo_vehiculo")
    @classmethod
    def validar_tipo(cls, v):
        if v not in ("bicicleta", "moto"):
            raise ValueError("tipo_vehiculo debe ser 'bicicleta' o 'moto'")
        return v

    @field_validator("valor_vehiculo")
    @classmethod
    def validar_valor(cls, v):
        if v < 500000:
            raise ValueError(
                "valor_vehiculo debe ser mayor o igual a $500,000"
            )
        return v

    @field_validator("cuota_inicial")
    @classmethod
    def validar_cuota_inicial(cls, v):
        if v < 0:
            raise ValueError("cuota_inicial no puede ser negativa")
        return v

    @field_validator("plazo_meses")
    @classmethod
    def validar_plazo(cls, v):
        if v < 1:
            raise ValueError("plazo_meses debe ser mayor a 0")
        return v

    @model_validator(mode="after")
    def validar_cuota_vs_valor(self):
        if self.cuota_inicial >= self.valor_vehiculo:
            raise ValueError(
                "cuota_inicial debe ser menor al valor del vehiculo"
            )
        return self


@simulacion_bp.route("/api/simulacion", methods=["POST"])
def simular():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "El cuerpo de la peticion debe ser JSON"}), 400

    try:
        req = SimulacionRequest.model_validate(data)
    except ValidationError as e:
        primer_error = e.errors()[0]["msg"]
        return jsonify({"error": primer_error}), 400

    tasa_anual = Decimal(str(Config.TASA_INTERES_ANUAL))
    resultado = calcular_amortizacion(
        req.valor_vehiculo, req.cuota_inicial, req.plazo_meses, tasa_anual
    )
    resumen = resultado["resumen"]

    simulacion = Simulacion(
        tipo_vehiculo=req.tipo_vehiculo,
        valor_vehiculo=req.valor_vehiculo,
        cuota_inicial=req.cuota_inicial,
        plazo_meses=req.plazo_meses,
        valor_financiado=Decimal(str(resumen["valor_financiado"])),
        cuota_mensual=Decimal(str(resumen["cuota_mensual"])),
        total_intereses=Decimal(str(resumen["total_intereses"])),
        total_pagar=Decimal(str(resumen["total_pagar"])),
    )
    db.session.add(simulacion)
    db.session.commit()

    return jsonify(
        {
            "id": simulacion.id,
            "resumen": resumen,
            "plan_pagos": resultado["plan_pagos"],
        }
    ), 200
