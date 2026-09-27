from datetime import datetime, time

def validar_id_bloqueo(id_bloqueo):
    if not str(id_bloqueo).isdigit() or int(id_bloqueo) <= 0:
        raise ValueError("El ID del bloqueo debe ser un entero positivo.")

    return int(id_bloqueo)

def validar_creacion_bloqueo(data):
    if not data:
        raise ValueError("El cuerpo de la solicitud no puede estar vacío.")

    campos_obligatorios = [
        "id_cancha",
        "fecha",
        "hora_inicio",
        "hora_fin"
    ]

    for campo in campos_obligatorios:
        if (
            campo not in data
            or data[campo] is None
            or str(data[campo]).strip() == ""
        ):
            raise ValueError(f"El campo '{campo}' es obligatorio.")
        
    try:
        id_cancha = int(data["id_cancha"])

        if id_cancha <= 0:
            raise ValueError()

    except (ValueError, TypeError):
        raise ValueError("El ID de la cancha debe ser un entero positivo.")

    try:
        fecha_obj = datetime.strptime(
            data["fecha"],
            "%Y-%m-%d"
        ).date()

    except ValueError:
        raise ValueError("La fecha debe tener el formato YYYY-MM-DD.")
    
    def parse_hora(h_str):
        for fmt in ("%H:%M:%S", "%H:%M"):
            try:
                return datetime.strptime(
                    str(h_str),
                    fmt
                ).time()

            except ValueError:
                pass

        raise ValueError(
            "Las horas deben tener el formato HH:MM:SS u HH:MM."
        )

    h_inicio = parse_hora(data["hora_inicio"])
    h_fin = parse_hora(data["hora_fin"])

    if h_inicio >= h_fin:
        raise ValueError(
            "La hora de inicio debe ser menor a la hora de fin."
        )

    hora_min = time(8, 0, 0)
    hora_max = time(23, 0, 0)

    if h_inicio < hora_min or h_fin > hora_max:
        raise ValueError(
            "El bloqueo debe estar dentro del horario operativo "
            "del club (08:00 a 23:00)."
        )

    return {
        "id_cancha": id_cancha,
        "fecha": str(fecha_obj),
        "hora_inicio": str(h_inicio),
        "hora_fin": str(h_fin),
        "motivo": data.get("motivo")
    }

def validar_y_obtener_filtros_bloqueos(args):
    filtros = {}

    if "id_cancha" in args and args["id_cancha"]:
        id_cancha = args["id_cancha"]

        if not str(id_cancha).isdigit() or int(id_cancha) <= 0:
            raise ValueError(
                "El ID de la cancha debe ser un entero positivo."
            )

        filtros["id_cancha"] = int(id_cancha)

    if "fecha" in args and args["fecha"]:
        fecha = args["fecha"]

        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            filtros["fecha"] = fecha

        except ValueError:
            raise ValueError(
                "La fecha debe tener el formato YYYY-MM-DD."
            )

    return filtros