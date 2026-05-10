from decimal import ROUND_HALF_UP, Decimal


def _redondear(valor: Decimal) -> Decimal:
    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calcular_amortizacion(
    valor_vehiculo: Decimal,
    cuota_inicial: Decimal,
    plazo_meses: int,
    tasa_anual: Decimal,
) -> dict:
    valor_financiado = valor_vehiculo - cuota_inicial
    i = tasa_anual / Decimal("12")

    factor = (Decimal("1") + i) ** plazo_meses
    cuota_mensual = _redondear(valor_financiado * i * factor / (factor - Decimal("1")))

    plan_pagos = []
    saldo = valor_financiado
    total_intereses = Decimal("0")

    for k in range(1, plazo_meses):
        interes = _redondear(saldo * i)
        abono = cuota_mensual - interes
        saldo -= abono
        total_intereses += interes

        plan_pagos.append(
            {
                "cuota_numero": k,
                "valor_cuota": float(cuota_mensual),
                "interes": float(interes),
                "abono_capital": float(abono),
                "saldo_restante": float(saldo),
            }
        )

    interes_final = _redondear(saldo * i)
    abono_final = saldo
    ultima_cuota = interes_final + abono_final
    total_intereses += interes_final

    plan_pagos.append(
        {
            "cuota_numero": plazo_meses,
            "valor_cuota": float(ultima_cuota),
            "interes": float(interes_final),
            "abono_capital": float(abono_final),
            "saldo_restante": 0.0,
        }
    )

    resumen = {
        "valor_vehiculo": float(valor_vehiculo),
        "cuota_inicial": float(cuota_inicial),
        "valor_financiado": float(valor_financiado),
        "cuota_mensual": float(cuota_mensual),
        "total_intereses": float(total_intereses),
        "total_pagar": float(valor_financiado + total_intereses),
        "plazo_meses": plazo_meses,
        "tasa_anual": float(tasa_anual),
    }

    return {"resumen": resumen, "plan_pagos": plan_pagos}
