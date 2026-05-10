from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

db = SQLAlchemy()


class Simulacion(db.Model):
    __tablename__ = "simulaciones"

    id = db.Column(db.Integer, primary_key=True)
    tipo_vehiculo = db.Column(db.String(20), nullable=False)
    valor_vehiculo = db.Column(db.Numeric(12, 2), nullable=False)
    cuota_inicial = db.Column(db.Numeric(12, 2), nullable=False)
    plazo_meses = db.Column(db.Integer, nullable=False)
    valor_financiado = db.Column(db.Numeric(12, 2), nullable=False)
    cuota_mensual = db.Column(db.Numeric(10, 2), nullable=False)
    total_intereses = db.Column(db.Numeric(10, 2), nullable=False)
    total_pagar = db.Column(db.Numeric(12, 2), nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    solicitudes = db.relationship("Solicitud", backref="simulacion", lazy=True)

    __table_args__ = (
        CheckConstraint(
            "tipo_vehiculo IN ('bicicleta', 'moto')",
            name="ck_simulaciones_tipo_vehiculo",
        ),
        CheckConstraint(
            "valor_vehiculo >= 500000",
            name="ck_simulaciones_valor_vehiculo",
        ),
        CheckConstraint(
            "plazo_meses > 0",
            name="ck_simulaciones_plazo_meses",
        ),
    )


class Solicitud(db.Model):
    __tablename__ = "solicitudes"

    id = db.Column(db.Integer, primary_key=True)
    simulacion_id = db.Column(
        db.Integer, db.ForeignKey("simulaciones.id"), nullable=False
    )
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
