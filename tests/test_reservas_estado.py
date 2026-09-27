from src.utils.time_utils import obtener_fechas_futuras
from src.database.connection import get_db_connection

def test_put_reserva_estado_transicion_invalida_devuelve_409(client):
    """Rechaza transiciones de estado no permitidas (ej. pasar de cancelada a confirmada)."""

    res_s = client.post(
        "/socios",
        json={
            "nombre": "Socio Inv",
            "email": "inv@test.com"
        }
    )

    res_c = client.post(
        "/canchas",
        json={
            "nombre": "Cancha Inv",
            "id_deporte": 1,
            "precio_hora": 1000000
        }
    )

    id_s = res_s.get_json()["id"]
    id_c = res_c.get_json()["id"]

    inicio, fin = obtener_fechas_futuras(
        dias_adelante=5,
        hora_inicio=16,
        duracion_horas=1
    )

    res_r = client.post(
        "/reservas",
        json={
            "id_socio": id_s,
            "id_cancha": id_c,
            "fecha_hora_inicio": inicio,
            "fecha_hora_fin": fin
        }
    )

    id_r = res_r.get_json()["id"]

    # 1. Cancelar la reserva
    client.put(
        f"/reservas/{id_r}/estado",
        json={"estado": "cancelada"}
    )

    # 2. Intentar cambiar de 'cancelada' a 'confirmada'
    response = client.put(
        f"/reservas/{id_r}/estado",
        json={"estado": "confirmada"}
    )

    assert response.status_code == 409

def test_put_reserva_estado_cancelar_y_liberar_horario_exito(client):
    """Cancela una reserva y verifica que el horario quede disponible para que otro socio pueda reservar."""

    # 1. Crear socios y cancha
    res_s1 = client.post(
        "/socios",
        json={
            "nombre": "Socio Canc 1",
            "email": "s1.canc@test.com"
        }
    )

    res_s2 = client.post(
        "/socios",
        json={
            "nombre": "Socio Canc 2",
            "email": "s2.canc@test.com"
        }
    )

    res_c = client.post(
        "/canchas",
        json={
            "nombre": "Cancha Liberada",
            "id_deporte": 1,
            "precio_hora": 1000000
        }
    )

    id_s1 = res_s1.get_json()["id"]
    id_s2 = res_s2.get_json()["id"]
    id_c = res_c.get_json()["id"]

    inicio, fin = obtener_fechas_futuras(
        dias_adelante=5,
        hora_inicio=10,
        duracion_horas=2
    )

    # 2. Crear reserva 1
    res_r1 = client.post(
        "/reservas",
        json={
            "id_socio": id_s1,
            "id_cancha": id_c,
            "fecha_hora_inicio": inicio,
            "fecha_hora_fin": fin
        }
    )

    id_r1 = res_r1.get_json()["id"]

    # 3. Cancelar reserva 1
    res_cancel = client.put(
        f"/reservas/{id_r1}/estado",
        json={"estado": "cancelada"}
    )

    assert res_cancel.status_code == 200
    assert res_cancel.get_json()["estado"] == "cancelada"

    # 4. Verificar que Socio 2 pueda reservar el mismo horario
    res_r2 = client.post(
        "/reservas",
        json={
            "id_socio": id_s2,
            "id_cancha": id_c,
            "fecha_hora_inicio": inicio,
            "fecha_hora_fin": fin
        }
    )

    assert res_r2.status_code == 201

def test_put_reserva_estado_finalizar_exito(client):
    """Transiciona exitosamente una reserva de confirmada a finalizada."""

    res_s = client.post(
        "/socios",
        json={
            "nombre": "Socio Fin",
            "email": "fin@test.com"
        }
    )

    res_c = client.post(
        "/canchas",
        json={
            "nombre": "Cancha Fin",
            "id_deporte": 1,
            "precio_hora": 1000000
        }
    )

    id_s = res_s.get_json()["id"]
    id_c = res_c.get_json()["id"]

    inicio, fin = obtener_fechas_futuras(
        dias_adelante=5,
        hora_inicio=12,
        duracion_horas=1
    )

    res_r = client.post(
        "/reservas",
        json={
            "id_socio": id_s,
            "id_cancha": id_c,
            "fecha_hora_inicio": inicio,
            "fecha_hora_fin": fin
        }
    )

    id_r = res_r.get_json()["id"]
    # se modifica directamente de la base de datos ya que tenemos que simular que pasó el tiempo para finalizar la reserva
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""UPDATE reservas 
                SET fecha_hora_inicio = '2020-01-01T10:00:00.000000-03:00',
                fecha_hora_fin = '2020-01-01T11:00:00.000000-03:00' WHERE id = %s""", (id_r)
            )
    finally:
        connection.close()


    response = client.put(
        f"/reservas/{id_r}/estado",
        json={"estado": "finalizada"}
    )

    assert response.status_code == 200
    assert response.get_json()["estado"] == "finalizada"

def test_put_reserva_estado_repetir_estado_actual_exito(client):
    """Enviar el mismo estado actual responde 200 OK sin producir alteraciones."""

    res_s = client.post(
        "/socios",
        json={
            "nombre": "Socio Rep",
            "email": "rep@test.com"
        }
    )

    res_c = client.post(
        "/canchas",
        json={
            "nombre": "Cancha Rep",
            "id_deporte": 1,
            "precio_hora": 1000000
        }
    )

    id_s = res_s.get_json()["id"]
    id_c = res_c.get_json()["id"]

    inicio, fin = obtener_fechas_futuras(
        dias_adelante=5,
        hora_inicio=14,
        duracion_horas=1
    )

    res_r = client.post(
        "/reservas",
        json={
            "id_socio": id_s,
            "id_cancha": id_c,
            "fecha_hora_inicio": inicio,
            "fecha_hora_fin": fin
        }
    )

    id_r = res_r.get_json()["id"]

    # Reenviar 'confirmada'
    response = client.put(
        f"/reservas/{id_r}/estado",
        json={"estado": "confirmada"}
    )

    assert response.status_code == 200
    assert response.get_json()["estado"] == "confirmada"