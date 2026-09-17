from src.repositories.canchas_repository import CanchasRepository
from src.repositories.canchas_repository import CanchasRepository
from src.repositories.deportes_repository import DeportesRepository

def obtener_canchas(filtros, limit, offset):
    canchas, total_records = CanchasRepository.buscar_canchas(filtros, limit, offset)

    for cancha in canchas:
        cancha["techada"] = bool(cancha["techada"])
        cancha["activa"] = bool(cancha["activa"])

    return canchas, total_records

def obtener_canchas(filtros, limit, offset):
    canchas, total_records = CanchasRepository.buscar_canchas(filtros, limit, offset)

    for cancha in canchas:
        cancha["techada"] = bool(cancha["techada"])
        cancha["activa"] = bool(cancha["activa"])

    return canchas, total_records

def crear_cancha(data):
    if not DeportesRepository.existe_deporte(data['id_deporte']):
        raise LookupError(f"El deporte asociado al id {data['id_deporte']} no existe.")

    CanchasRepository.crear_cancha(data)