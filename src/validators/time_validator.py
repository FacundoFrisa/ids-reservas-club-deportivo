import re
from datetime import datetime, timezone, timedelta

REGEX_ISO_8601_GMT3 = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}-03:00$'

def validar_intervalo_reserva(inicio_str, fin_str):
    if not isinstance(inicio_str, str) or not re.match(REGEX_ISO_8601_GMT3, inicio_str):
        raise ValueError("El inicio debe tener el formato estricto YYYY-MM-DDTHH:MM:SS.ffffff-03:00")
    
    if not isinstance(fin_str, str) or not re.match(REGEX_ISO_8601_GMT3, fin_str):
        raise ValueError("El fin debe tener el formato estricto YYYY-MM-DDTHH:MM:SS.ffffff-03:00")

    formato_str = "%Y-%m-%dT%H:%M:%S.%f"
    try:
        inicio_dt = datetime.strptime(inicio_str[:-6], formato_str)
        fin_dt = datetime.strptime(fin_str[:-6], formato_str)
    except ValueError:
        raise ValueError("Las fechas proporcionadas no existen en el calendario.")

    if inicio_dt.minute != 0 or inicio_dt.second != 0 or inicio_dt.microsecond != 0:
        raise ValueError("El horario de inicio debe ser una hora en punto (ej. 18:00:00.000000-03:00).")
    
    if fin_dt.minute != 0 or fin_dt.second != 0 or fin_dt.microsecond != 0:
        raise ValueError("El horario de fin debe ser una hora en punto (ej. 20:00:00.000000-03:00).")

    if inicio_dt >= fin_dt:
        raise ValueError("La fecha y hora de inicio debe ser estrictamente anterior a la de fin.")
    
    if inicio_dt.date() != fin_dt.date():
        raise ValueError("La reserva debe comenzar y terminar en el mismo día, no puede atravesar la medianoche.")

    if inicio_dt.hour < 8 or fin_dt.hour > 23 or (fin_dt.hour == 23 and fin_dt.minute > 0):
        raise ValueError("El intervalo solicitado se encuentra fuera del horario de atención del club (08:00 a 23:00).")

    duracion_horas = (fin_dt - inicio_dt).total_seconds() / 3600
    if duracion_horas not in [1.0, 2.0, 3.0]:
        raise ValueError("Las reservas deben tener una duración exacta de 1, 2 o 3 horas.")

    ahora_gmt3 = datetime.now(timezone.utc) - timedelta(hours=3)
    ahora_gmt3 = ahora_gmt3.replace(tzinfo=None)
    
    if inicio_dt <= ahora_gmt3:
        raise ValueError("El horario de inicio de la reserva debe ser estrictamente en el futuro.")

    return inicio_dt, fin_dt