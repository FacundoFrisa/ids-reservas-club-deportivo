from src.repositories.bloqueos_repository import BloqueosRepository
from src.repositories.canchas_repository import CanchasRepository
from src.errors.exceptions import NotFoundError, ConflictError

def crear_bloqueo(datos):
    cancha = CanchasRepository.obtener_cancha_por_id(datos["id_cancha"])

    if not cancha:
        raise NotFoundError("La cancha solicitada no existe.")
    
    hay_superposicion = BloqueosRepository.existe_superposicion(
        datos["id_cancha"], 
        datos["fecha"], 
        datos["hora_inicio"], 
        datos["hora_fin"]
    )
    
    if hay_superposicion:
        raise ConflictError("No se puede crear el bloqueo porque ya existe una reserva o un mantenimiento confirmado en ese intervalo de horario para esta cancha.")

    nuevo_id = BloqueosRepository.crear_bloqueo(datos)
    datos["id"] = nuevo_id
    return datos

def obtener_bloqueos(filtros, limit, offset):
    bloqueos, total = BloqueosRepository.obtener_bloqueos(filtros, limit, offset)

    for bloqueo in bloqueos:
        if "fecha" in bloqueo and bloqueo["fecha"] is not None:
            bloqueo["fecha"] = str(bloqueo["fecha"])
        if "hora_inicio" in bloqueo and bloqueo["hora_inicio"] is not None:
            bloqueo["hora_inicio"] = str(bloqueo["hora_inicio"])
        if "hora_fin" in bloqueo and bloqueo["hora_fin"] is not None:
            bloqueo["hora_fin"] = str(bloqueo["hora_fin"])
            
    return bloqueos, total

def eliminar_bloqueo(bloqueo_id):
    eliminado = BloqueosRepository.eliminar_bloqueo(bloqueo_id)
    if not eliminado:
        raise NotFoundError(f"El bloqueo con id {bloqueo_id} no existe.")
    return True