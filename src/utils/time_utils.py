from datetime import datetime, timedelta

def obtener_fechas_futuras(
    dias_adelante=3,
    hora_inicio=10,
    duracion_horas=2
):
    """Genera fechas/horas futuras dinámicas en formato ISO 8601 (GMT-3)."""
    fecha_base = datetime.now() + timedelta(days=dias_adelante)

    inicio_dt = fecha_base.replace(
        hour=hora_inicio,
        minute=0,
        second=0,
        microsecond=0
    )

    fin_dt = inicio_dt + timedelta(hours=duracion_horas)

    inicio_iso = inicio_dt.strftime("%Y-%m-%dT%H:%M:%S.000000-03:00")
    fin_iso = fin_dt.strftime("%Y-%m-%dT%H:%M:%S.000000-03:00")

    return inicio_iso, fin_iso