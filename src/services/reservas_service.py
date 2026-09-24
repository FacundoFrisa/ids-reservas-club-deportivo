from src.repositories.reservas_repository import ReservasRepository
from src.errors.exceptions import NotFoundError


def obtener_reservas(filtros, limit, offset):
    reservas, total_records = ReservasRepository.buscar_reservas(
        filtros,
        limit,
        offset
    )

    return reservas, total_records

def obtener_reserva_por_id(id_reserva):
    reserva = ReservasRepository.obtener_reserva_por_id(id_reserva)

    if not reserva:
        raise NotFoundError(
            f"La reserva con id {id_reserva} no existe."
        )

    return reserva