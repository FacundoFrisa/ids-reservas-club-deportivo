import re

PARAMETROS_PERMITIDOS = {
    "nombre",
    "activo",
    "_limit",
    "_offset"
}

CAMPOS_PERMITIDOS_POST = {"nombre", "email"}
REGEX_EMAIL = r"^[\w\.-]+@[\w\.-]+\.\w+$"

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

def validar_creacion_socio(data):
    if not data or not isinstance(data, dict):
        raise ValueError(
            "El cuerpo de la solicitud debe ser un objeto JSON no vacío."
        )
    
    desconocidos = set(data.keys()) - CAMPOS_PERMITIDOS_POST

    if desconocidos:
        raise ValueError(
            f"Se rechazan campos no permitidos: {', '.join(desconocidos)}"
        )

    if "nombre" not in data or "email" not in data:
        raise ValueError(
            "Los campos 'nombre' y 'email' son obligatorios."
        )

    nombre = data["nombre"]
    email = data["email"]

    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El campo 'nombre' no puede quedar vacío.")
    
    if not isinstance(email, str):
        raise ValueError(
            "El campo 'email' debe ser una cadena de texto."
        )

    email_limpio = email.strip().lower()

    if not re.match(REGEX_EMAIL, email_limpio):
        raise ValueError(
            f"El correo electrónico '{email}' no tiene un formato válido."
        )

    return {
        "nombre": nombre.strip(),
        "email": email_limpio,
    }