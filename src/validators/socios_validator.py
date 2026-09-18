PARAMETROS_PERMITIDOS = {
    "nombre",
    "activo",
    "_limit",
    "_offset"
}


def validar_y_obtener_filtros_socios(args):
    desconocidos = set(args.keys()) - PARAMETROS_PERMITIDOS

    if desconocidos:
        raise ValueError(
            f"Parámetro(s) no permitido(s): {', '.join(desconocidos)}"
        )

    filtros = {}

    if "nombre" in args:
        nombre = args["nombre"].strip()

        if nombre:
            filtros["nombre"] = nombre

    if "activo" in args:
        val = args["activo"].lower()

        if val == "true":
            filtros["activo"] = True

        elif val == "false":
            filtros["activo"] = False

        else:
            raise ValueError(
                "El parámetro 'activo' admite únicamente true o false."
            )

    return filtros


def validar_id_socio(id_socio):
    if id_socio <= 0:
        raise ValueError(
            "El ID del socio debe ser un entero positivo."
        )