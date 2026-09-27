from src.repositories.bloqueos_repository import BloqueosRepository

def crear_bloqueo(datos):
    if not datos.get("id_cancha") or not datos.get("fecha") or not datos.get("hora_inicio") or not datos.get("hora_fin"):
        raise ValueError("Todos los campos obligatorios deben estar completos.")
    
    if datos["hora_inicio"] >= datos["hora_fin"]:
        raise ValueError("La hora de inicio debe ser menor a la hora de fin.")

    hay_superposicion = BloqueosRepository.existe_superposicion(
        datos["id_cancha"], 
        datos["fecha"], 
        datos["hora_inicio"], 
        datos["hora_fin"]
    )
    
    if hay_superposicion:
        raise ValueError("No se puede crear el bloqueo porque ya existe una reserva o un mantenimiento confirmado en ese intervalo de horario para esta cancha.")

    nuevo_id = BloqueosRepository.crear_bloqueo(datos)
    datos["id"] = nuevo_id
    return datos

def obtener_bloqueos(filtros, limit, offset):
    bloqueos, total = BloqueosRepository.obtener_bloqueos(filtros, limit, offset)

    for bloqueo in bloqueos:
        if "hora_inicio" in bloqueo and bloqueo["hora_inicio"] is not None:
            bloqueo["hora_inicio"] = str(bloqueo["hora_inicio"])
        if "hora_fin" in bloqueo and bloqueo["hora_fin"] is not None:
            bloqueo["hora_fin"] = str(bloqueo["hora_fin"])
            
    return bloqueos, total

def eliminar_bloqueo(bloqueo_id):
    eliminado = BloqueosRepository.eliminar_bloqueo(bloqueo_id)
    if not eliminado:
        raise LookupError("El bloqueo especificado no existe.")
    return True