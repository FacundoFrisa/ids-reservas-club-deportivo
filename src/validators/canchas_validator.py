PARAMETROS_PERMITIDOS = {
    'id_deporte',
    'nombre',
    'techada',
    'activa',
    '_limit',
    '_offset'
}

def validar_y_obtener_filtros_canchas(args):
    desconocidos = set(args.keys()) - PARAMETROS_PERMITIDOS

    if desconocidos:
        raise ValueError(
            f"Parámetro(s) no permitido(s): {', '.join(desconocidos)}"
        )

    filtros = {}

    if 'id_deporte' in args:
        try:
            filtros['id_deporte'] = int(args.get('id_deporte'))
        except ValueError:
            raise ValueError(
                "El parámetro 'id_deporte' debe ser un número entero."
            )

    if 'nombre' in args:
        filtros['nombre'] = args.get('nombre')

    for bool_filter in ['techada', 'activa']:
        if bool_filter in args:
            val = args.get(bool_filter)

            if val not in ['true', 'false']:
                raise ValueError(
                    f"El filtro '{bool_filter}' solo admite 'true' o 'false'."
                )

            filtros[bool_filter] = val

    return filtros