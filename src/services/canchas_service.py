from src.repositories.canchas_repository import CanchasRepository

def obtener_canchas(filtros, limit, offset):
    canchas, total_records = CanchasRepository.buscar_canchas(filtros, limit, offset)

    for cancha in canchas:
        cancha["techada"] = bool(cancha["techada"])
        cancha["activa"] = bool(cancha["activa"])

    return canchas, total_records