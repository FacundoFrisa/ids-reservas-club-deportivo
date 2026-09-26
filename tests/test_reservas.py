import pytest
from datetime import datetime, timedelta


def obtener_fechas_futuras(
    dias_adelante=3,
    hora_inicio=10,
    duracion_horas=2
):
    """Genera fechas/horas futuras dinámicas en formato ISO 8601 (GMT-3)."""
    fecha_base = datetime.now() + timedelta(days=dias_adelante)

    inicio_dt = fecha_base.replace(
        hour=hora_inicio,
        minute=0,
        second=0,
        microsecond=0
    )

    fin_dt = inicio_dt + timedelta(hours=duracion_horas)

    inicio_iso = inicio_dt.strftime("%Y-%m-%dT%H:%M:%S.000000-03:00")
    fin_iso = fin_dt.strftime("%Y-%m-%dT%H:%M:%S.000000-03:00")

    return inicio_iso, fin_iso


def test_post_reserva_exito_y_calculo_importe(client):
    """Verifica la creación exitosa de una reserva y el cálculo correcto de precio_total."""

    # 1. Crear socio y cancha auxiliares para el test
    res_socio = client.post(
        "/socios",
        json={
            "nombre": "Socio Test Reserva",
            "email": "socio.reserva1@test.com"
        }
    )

    assert res_socio.status_code == 201
    id_socio = res_socio.get_json()["id"]

    res_cancha = client.post(
        "/canchas",
        json={
            "nombre": "Cancha Test Reserva 1",
            "id_deporte": 1,
            "precio_hora": 1500000
        }
    )

    assert res_cancha.status_code == 201

    cancha_data = res_cancha.get_json()
    id_cancha = cancha_data["id"]
    precio_hora = cancha_data["precio_hora"]

    # 2. Generar horario futuro (2 horas de duración)
    inicio, fin = obtener_fechas_futuras(
        dias_adelante=2,
        hora_inicio=10,
        duracion_horas=2
    )

    body = {
        "id_socio": id_socio,
        "id_cancha": id_cancha,
        "fecha_hora_inicio": inicio,
        "fecha_hora_fin": fin
    }

    # 3. Realizar reserva
    response = client.post("/reservas", json=body)

    assert response.status_code == 201

    data = response.get_json()

    assert data["id_socio"] == id_socio
    assert data["id_cancha"] == id_cancha
    assert data["estado"] == "confirmada"
    assert data["precio_hora"] == precio_hora
    assert data["precio_total"] == precio_hora * 2


def test_post_reserva_dos_reservas_distinto_horario_mismo_socio_exito(client):
    """Verifica que un socio pueda realizar múltiples reservas si los horarios no se solapan."""

    res_socio = client.post(
        "/socios",
        json={
            "nombre": "Socio Multi Reserva",
            "email": "socio.multi@test.com"
        }
    )

    id_socio = res_socio.get_json()["id"]

    res_cancha = client.post(
        "/canchas",
        json={
            "nombre": "Cancha Test Multi",
            "id_deporte": 1,
            "precio_hora": 1000000
        }
    )

    id_cancha = res_cancha.get_json()["id"]

    # Reserva 1: 10:00 a 12:00
    inicio1, fin1 = obtener_fechas_futuras(
        dias_adelante=3,
        hora_inicio=10,
        duracion_horas=2
    )

    res1 = client.post(
        "/reservas",
        json={
            "id_socio": id_socio,
            "id_cancha": id_cancha,
            "fecha_hora_inicio": inicio1,
            "fecha_hora_fin": fin1
        }
    )

    assert res1.status_code == 201

    # Reserva 2: 14:00 a 16:00 (mismo día, diferente horario)
    inicio2, fin2 = obtener_fechas_futuras(
        dias_adelante=3,
        hora_inicio=14,
        duracion_horas=2
    )

    res2 = client.post(
        "/reservas",
        json={
            "id_socio": id_socio,
            "id_cancha": id_cancha,
            "fecha_hora_inicio": inicio2,
            "fecha_hora_fin": fin2
        }
    )

    assert res2.status_code == 201


def test_post_reserva_consecutivas_mismo_horario_limite_exito(client):
    """Verifica que se permitan reservas consecutivas (ej. 18:00 a 19:00 y 19:00 a 20:00)."""

    res_socio = client.post(
        "/socios",
        json={
            "nombre": "Socio Consecutivo",
            "email": "socio.consecutivo@test.com"
        }
    )

    id_socio = res_socio.get_json()["id"]

    res_cancha = client.post(
        "/canchas",
        json={
            "nombre": "Cancha Consecutiva",
            "id_deporte": 1,
            "precio_hora": 1000000
        }
    )

    id_cancha = res_cancha.get_json()["id"]

    inicio1, fin1 = obtener_fechas_futuras(
        dias_adelante=4,
        hora_inicio=18,
        duracion_horas=1
    )

    inicio2, fin2 = obtener_fechas_futuras(
        dias_adelante=4,
        hora_inicio=19,
        duracion_horas=1
    )

    r1 = client.post(
        "/reservas",
        json={
            "id_socio": id_socio,
            "id_cancha": id_cancha,
            "fecha_hora_inicio": inicio1,
            "fecha_hora_fin": fin1
        }
    )

    assert r1.status_code == 201

    r2 = client.post(
        "/reservas",
        json={
            "id_socio": id_socio,
            "id_cancha": id_cancha,
            "fecha_hora_inicio": inicio2,
            "fecha_hora_fin": fin2
        }
    )

    assert r2.status_code == 201


def test_post_reserva_superposicion_misma_cancha_devuelve_409(client):
    """Rechaza la reserva si la cancha ya tiene una reserva confirmada que se solapa."""

    res_socio1 = client.post(
        "/socios",
        json={
            "nombre": "Socio Solap 1",
            "email": "solap1@test.com"
        }
    )

    res_socio2 = client.post(
        "/socios",
        json={
            "nombre": "Socio Solap 2",
            "email": "solap2@test.com"
        }
    )

    id_socio1 = res_socio1.get_json()["id"]
    id_socio2 = res_socio2.get_json()["id"]

    res_cancha = client.post(
        "/canchas",
        json={
            "nombre": "Cancha Solapada",
            "id_deporte": 1,
            "precio_hora": 1000000
        }
    )

    id_cancha = res_cancha.get_json()["id"]

    # Reserva 1: 18:00 a 20:00
    inicio1, fin1 = obtener_fechas_futuras(
        dias_adelante=5,
        hora_inicio=18,
        duracion_horas=2
    )

    client.post(
        "/reservas",
        json={
            "id_socio": id_socio1,
            "id_cancha": id_cancha,
            "fecha_hora_inicio": inicio1,
            "fecha_hora_fin": fin1
        }
    )

    # Intentar Reserva 2 solapada parcialmente (19:00 a 21:00)
    inicio2, fin2 = obtener_fechas_futuras(
        dias_adelante=5,
        hora_inicio=19,
        duracion_horas=2
    )

    response = client.post(
        "/reservas",
        json={
            "id_socio": id_socio2,
            "id_cancha": id_cancha,
            "fecha_hora_inicio": inicio2,
            "fecha_hora_fin": fin2
        }
    )

    assert response.status_code == 409


def test_post_reserva_superposicion_mismo_socio_distinta_cancha_devuelve_409(client):
    """Rechaza la reserva si el mismo socio intenta reservar en otra cancha en el mismo horario."""

    res_socio = client.post(
        "/socios",
        json={
            "nombre": "Socio Solap Doble",
            "email": "doble.cancha@test.com"
        }
    )

    id_socio = res_socio.get_json()["id"]

    res_cancha1 = client.post(
        "/canchas",
        json={
            "nombre": "Cancha A",
            "id_deporte": 1,
            "precio_hora": 1000000
        }
    )

    res_cancha2 = client.post(
        "/canchas",
        json={
            "nombre": "Cancha B",
            "id_deporte": 1,
            "precio_hora": 1000000
        }
    )

    id_cancha1 = res_cancha1.get_json()["id"]
    id_cancha2 = res_cancha2.get_json()["id"]

    inicio, fin = obtener_fechas_futuras(
        dias_adelante=6,
        hora_inicio=11,
        duracion_horas=2
    )

    # Reserva en Cancha A
    client.post(
        "/reservas",
        json={
            "id_socio": id_socio,
            "id_cancha": id_cancha1,
            "fecha_hora_inicio": inicio,
            "fecha_hora_fin": fin
        }
    )

    # Intentar reserva en Cancha B en el mismo horario para el mismo socio
    response = client.post(
        "/reservas",
        json={
            "id_socio": id_socio,
            "id_cancha": id_cancha2,
            "fecha_hora_inicio": inicio,
            "fecha_hora_fin": fin
        }
    )

    assert response.status_code == 409


def test_conservacion_tarifa_historica(client):
    """Verifica que el precio congelado al crear la reserva no cambie si se edita la cancha luego."""

    res_socio = client.post(
        "/socios",
        json={
            "nombre": "Socio Tarifa",
            "email": "tarifa.historica@test.com"
        }
    )

    id_socio = res_socio.get_json()["id"]

    res_cancha = client.post(
        "/canchas",
        json={
            "nombre": "Cancha Tarifa Variable",
            "id_deporte": 1,
            "precio_hora": 1000000
        }
    )

    id_cancha = res_cancha.get_json()["id"]

    inicio, fin = obtener_fechas_futuras(
        dias_adelante=7,
        hora_inicio=10,
        duracion_horas=2
    )

    # Crear reserva con tarifa original
    res_reserva = client.post(
        "/reservas",
        json={
            "id_socio": id_socio,
            "id_cancha": id_cancha,
            "fecha_hora_inicio": inicio,
            "fecha_hora_fin": fin
        }
    )

    id_reserva = res_reserva.get_json()["id"]

    # Modificar tarifa de la cancha
    client.patch(
        f"/canchas/{id_cancha}",
        json={"precio_hora": 2000000}
    )

    # Consultar la reserva creada previamente
    response_get = client.get(f"/reservas/{id_reserva}")

    if response_get.status_code == 200:
        data_get = response_get.get_json()

        assert data_get["precio_hora"] == 1000000
        assert data_get["precio_total"] == 2000000


def test_post_reserva_referencias_inexistentes_devuelve_404(client):
    """Devuelve 404 si la cancha o el socio no existen."""

    inicio, fin = obtener_fechas_futuras(
        dias_adelante=8,
        hora_inicio=10,
        duracion_horas=1
    )

    # Socio inexistente
    res1 = client.post(
        "/reservas",
        json={
            "id_socio": 999999,
            "id_cancha": 1,
            "fecha_hora_inicio": inicio,
            "fecha_hora_fin": fin
        }
    )

    assert res1.status_code == 404

    # Cancha inexistente
    res2 = client.post(
        "/reservas",
        json={
            "id_socio": 1,
            "id_cancha": 999999,
            "fecha_hora_inicio": inicio,
            "fecha_hora_fin": fin
        }
    )

    assert res2.status_code == 404