from src.repositories.socios_repository import SociosRepository

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