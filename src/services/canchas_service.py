from src.repositories.canchas_repository import CanchasRepository
from src.repositories.canchas_repository import CanchasRepository
from src.repositories.deportes_repository import DeportesRepository
from src.errors.exceptions import NotFoundError, ConflictError

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

    return CanchasRepository.crear_cancha(data)
    
def obtener_cancha_por_id(id_cancha):
    cancha = CanchasRepository.obtener_cancha_por_id(id_cancha)
    if not cancha:
        raise NotFoundError(f"La cancha con id {id_cancha} no existe.")
    
    cancha["techada"] = bool(cancha["techada"])
    cancha["activa"] = bool(cancha["activa"])
    return cancha

def actualizar_cancha(id_cancha, data):
    obtener_cancha_por_id(id_cancha)
    CanchasRepository.actualizar_cancha(id_cancha, data)
    
def eliminar_cancha(id_cancha):
    obtener_cancha_por_id(id_cancha)
    
    if CanchasRepository.tiene_reservas(id_cancha):
        raise ConflictError("No se puede eliminar la cancha porque tiene reservas asociadas.")
        
    CanchasRepository.eliminar_cancha(id_cancha)
    
def obtener_canchas_disponibles(filtros, limit, offset):
    canchas, total_records = CanchasRepository.buscar_canchas_disponibles(filtros, limit, offset)

    for cancha in canchas:
        cancha["techada"] = bool(cancha["techada"])
        cancha["activa"] = bool(cancha["activa"])

    return canchas, total_records