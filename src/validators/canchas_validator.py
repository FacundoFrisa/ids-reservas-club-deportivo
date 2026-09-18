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

def validar_creacion_cancha(data):
    if not isinstance(data, dict):
        raise ValueError("El cuerpo de la solicitud debe ser un objeto JSON válido.")

    permitidos = {'nombre', 'id_deporte', 'precio_hora', 'techada', 'activa'}
    desconocidos = set(data.keys()) - permitidos
    if desconocidos:
        raise ValueError(f"Se rechazan campos desconocidos: {', '.join(desconocidos)}")

    obligatorios = ['nombre', 'id_deporte', 'precio_hora']
    for campo in obligatorios:
        if campo not in data:
            raise ValueError(f"El campo '{campo}' es obligatorio.")

    if type(data['nombre']) is not str:
        raise ValueError("El nombre debe ser una cadena de texto.")
    
    nombre_limpio = data['nombre'].strip()
    if not nombre_limpio:
        raise ValueError("El nombre no podrá quedar vacío después de quitar espacios.")
    data['nombre'] = nombre_limpio

    if type(data['id_deporte']) is not int or data['id_deporte'] <= 0:
        raise ValueError("El id_deporte debe ser un entero positivo.")

    if type(data['precio_hora']) is not int or data['precio_hora'] <= 0:
        raise ValueError("El precio_hora debe ser un entero positivo en centavos.")

    if 'techada' in data:
        if type(data['techada']) is not bool:
            raise ValueError("El campo 'techada' admite únicamente true o false.")
    else:
        data['techada'] = False

    if 'activa' in data:
        if type(data['activa']) is not bool:
            raise ValueError("El campo 'activa' admite únicamente true o false.")
    else:
        data['activa'] = True

    return data

def validar_actualizacion_cancha(data):
    if not isinstance(data, dict) or not data:
        raise ValueError("El cuerpo de la solicitud en actualizaciones no puede estar vacío.")
    
    permitidos = {'nombre', 'precio_hora', 'techada', 'activa'}
    desconocidos = set(data.keys()) - permitidos
    if desconocidos:
        raise ValueError(f"Campos no permitidos o inmutables en la actualización: {', '.join(desconocidos)}")

    if 'nombre' in data:
        if type(data['nombre']) is not str:
            raise ValueError("El nombre debe ser una cadena de texto.")
        nombre_limpio = data['nombre'].strip()
        if not nombre_limpio:
            raise ValueError("El nombre no podrá quedar vacío después de quitar espacios.")
        data['nombre'] = nombre_limpio

    if 'precio_hora' in data:
        if type(data['precio_hora']) is not int or data['precio_hora'] <= 0:
            raise ValueError("The precio_hora debe ser un entero positivo en centavos.")

    if 'techada' in data:
        if type(data['techada']) is not bool:
            raise ValueError("El campo 'techada' admite únicamente true o false.")

    if 'activa' in data:
        if type(data['activa']) is not bool:
            raise ValueError("El campo 'activa' admite únicamente true o false.")

    return data