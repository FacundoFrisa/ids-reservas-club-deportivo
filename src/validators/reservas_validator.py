from datetime import datetime


PARAMETROS_PERMITIDOS = {
    'id_cancha',
    'id_socio',
    'estado',
    'fecha_desde',
    'fecha_hasta',
    '_limit',
    '_offset'
}

ESTADOS_VALIDOS = {
    'confirmada',
    'cancelada',
    'finalizada'
}


def validar_y_obtener_filtros_reservas(args):
    desconocidos = set(args.keys()) - PARAMETROS_PERMITIDOS

    if desconocidos:
        raise ValueError(
            f"Parámetro(s) no permitido(s): {', '.join(desconocidos)}"
        )

    filtros = {}

    if 'id_cancha' in args:
        try:
            id_cancha = int(args.get('id_cancha'))

            if id_cancha <= 0:
                raise ValueError

            filtros['id_cancha'] = id_cancha

        except ValueError:
            raise ValueError(
                "El parámetro 'id_cancha' debe ser un entero positivo."
            )

    if 'id_socio' in args:
        try:
            id_socio = int(args.get('id_socio'))

            if id_socio <= 0:
                raise ValueError

            filtros['id_socio'] = id_socio

        except ValueError:
            raise ValueError(
                "El parámetro 'id_socio' debe ser un entero positivo."
            )

    if 'estado' in args:
        estado = args.get('estado')

        if estado not in ESTADOS_VALIDOS:
            raise ValueError(
                "El parámetro 'estado' debe ser "
                "'confirmada', 'cancelada' o 'finalizada'."
            )

        filtros['estado'] = estado

    if 'fecha_desde' in args:
        fecha_desde = args.get('fecha_desde')

        try:
            datetime.strptime(fecha_desde, '%Y-%m-%d')
        except ValueError:
            raise ValueError(
                "El parámetro 'fecha_desde' debe tener "
                "el formato YYYY-MM-DD y ser una fecha válida."
            )

        filtros['fecha_desde'] = fecha_desde

    if 'fecha_hasta' in args:
        fecha_hasta = args.get('fecha_hasta')

        try:
            datetime.strptime(fecha_hasta, '%Y-%m-%d')
        except ValueError:
            raise ValueError(
                "El parámetro 'fecha_hasta' debe tener "
                "el formato YYYY-MM-DD y ser una fecha válida."
            )

        filtros['fecha_hasta'] = fecha_hasta

    if 'fecha_desde' in filtros and 'fecha_hasta' in filtros:
        if filtros['fecha_desde'] > filtros['fecha_hasta']:
            raise ValueError(
                "El parámetro 'fecha_desde' no puede ser posterior "
                "a 'fecha_hasta'."
            )

    return filtros