from src.repositories.reservas_repository import ReservasRepository


def obtener_reservas(filtros, limit, offset):
    reservas, total_records = ReservasRepository.buscar_reservas(
        filtros,
        limit,
        offset
    )

    return reservas, total_records