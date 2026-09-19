from src.repositories.socios_repository import SociosRepository
from src.errors.exceptions import ConflictError

def obtener_socios(filtros, limit, offset):
    return SociosRepository.obtener_socios(
        filtros,
        limit,
        offset
    )


def obtener_socio_por_id(id_socio):
    socio = SociosRepository.obtener_socio_por_id(id_socio)

    if not socio:
        raise LookupError(
            f"El socio con ID {id_socio} no existe."
        )

    return socio

def crear_socio(datos_socio):
    email = datos_socio["email"]

    if SociosRepository.existe_email(email):
        raise ConflictError(
            f"El correo electrónico '{email}' ya se encuentra registrado."
        )

    return SociosRepository.crear_socio(
        datos_socio["nombre"],
        email,
    )