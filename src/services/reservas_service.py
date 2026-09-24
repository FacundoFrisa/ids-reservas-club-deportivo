from src.repositories.reservas_repository import ReservasRepository
from src.errors.exceptions import NotFoundError, ConflictError
from datetime import datetime

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

def crear_reserva(datos):
    cancha, socio = ReservasRepository.verificar_cancha_y_socio(
        datos['id_cancha'], datos['id_socio']
    )

    if not cancha:
        raise NotFoundError("La cancha solicitada no existe.")
    if not socio:
        raise NotFoundError("El socio solicitado no existe.")

    if not cancha.get('activa'):
        raise ConflictError("La cancha se encuentra inactiva.")
    if not socio.get('activo'):
        raise ConflictError("El socio se encuentra inactivo.")
    
    conflicto = ReservasRepository.verificar_superposicion(
        datos['id_cancha'],
        datos['id_socio'],
        datos['fecha_hora_inicio'],
        datos['fecha_hora_fin']
    )

    if conflicto:
        if conflicto['id_cancha'] == datos['id_cancha']:
            raise ConflictError("La cancha ya tiene una reserva confirmada que se superpone con el horario solicitado.")
        else:
            raise ConflictError("El socio ya tiene una reserva confirmada en ese horario en otra cancha.")

    inicio_dt = datetime.strptime(datos['fecha_hora_inicio'][:-6], "%Y-%m-%dT%H:%M:%S.%f")
    fin_dt = datetime.strptime(datos['fecha_hora_fin'][:-6], "%Y-%m-%dT%H:%M:%S.%f")
    horas = int((fin_dt - inicio_dt).total_seconds() / 3600)
    
    precio_hora = cancha['precio_hora']
    precio_total = horas * precio_hora

    nueva_reserva = {
        'id_socio': datos['id_socio'],
        'id_cancha': datos['id_cancha'],
        'fecha_hora_inicio': datos['fecha_hora_inicio'],
        'fecha_hora_fin': datos['fecha_hora_fin'],
        'estado': 'confirmada',
        'precio_hora': precio_hora,
        'precio_total': precio_total
    }

    reserva_id = ReservasRepository.crear_reserva(nueva_reserva)
    nueva_reserva['id'] = reserva_id
    
    return nueva_reserva