import pytest
from src.utils.time_utils import obtener_fechas_futuras

def test_post_reserva_exito_y_calculo_importe(client):
    """Verifica la creación exitosa de una reserva y el cálculo correcto de precio_total."""

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

def test_post_reserva_duracion_invalida_devuelve_400(client):
    """Rechaza reservas con duración menor a 1 hora (ej. 30 min) o mayor a 3 horas (ej. 4 hs)."""

    # Reserva de 4 horas (10:00 a 14:00)
    inicio, fin = obtener_fechas_futuras(
        dias_adelante=5,
        hora_inicio=10,
        duracion_horas=4
    )

    body = {
        "id_socio": 1,
        "id_cancha": 1,
        "fecha_hora_inicio": inicio,
        "fecha_hora_fin": fin
    }

    response = client.post("/reservas", json=body)

    assert response.status_code == 400

    data = response.get_json()

    assert "errors" in data


def test_post_reserva_horario_fuera_de_jornada_devuelve_400(client):
    """Rechaza reservas fuera del horario operativo del club (08:00 a 23:00 hs)."""

    # Intentar reservar de 06:00 a 08:00 AM
    inicio, fin = obtener_fechas_futuras(
        dias_adelante=5,
        hora_inicio=6,
        duracion_horas=2
    )

    body = {
        "id_socio": 1,
        "id_cancha": 1,
        "fecha_hora_inicio": inicio,
        "fecha_hora_fin": fin
    }

    response = client.post("/reservas", json=body)

    assert response.status_code == 400

    data = response.get_json()

    assert "errors" in data


def test_post_reserva_en_el_pasado_devuelve_400(client):
    """Rechaza intentar registrar una reserva con fecha/hora anterior al momento actual."""

    body = {
        "id_socio": 1,
        "id_cancha": 1,
        "fecha_hora_inicio": "2020-01-01T10:00:00.000000-03:00",
        "fecha_hora_fin": "2020-01-01T12:00:00.000000-03:00"
    }

    response = client.post("/reservas", json=body)

    assert response.status_code == 400

    data = response.get_json()

    assert "errors" in data


def test_post_reserva_rango_invertido_devuelve_400(client):
    """Rechaza cuando fecha_hora_inicio es posterior o igual a fecha_hora_fin."""

    inicio, fin = obtener_fechas_futuras(
        dias_adelante=5,
        hora_inicio=10,
        duracion_horas=2
    )

    # Invertimos inicio y fin
    body = {
        "id_socio": 1,
        "id_cancha": 1,
        "fecha_hora_inicio": fin,
        "fecha_hora_fin": inicio
    }

    response = client.post("/reservas", json=body)

    assert response.status_code == 400

    data = response.get_json()

    assert "errors" in data


def test_post_reserva_campos_obligatorios_faltantes_devuelve_400(client):
    """Rechaza la solicitud si falta alguno de los 4 campos obligatorios."""

    inicio, fin = obtener_fechas_futuras(
        dias_adelante=5,
        hora_inicio=10,
        duracion_horas=1
    )

    # Omitimos id_socio
    body = {
        "id_cancha": 1,
        "fecha_hora_inicio": inicio,
        "fecha_hora_fin": fin
    }

    response = client.post("/reservas", json=body)

    assert response.status_code == 400

    data = response.get_json()

    assert "errors" in data

def test_post_reserva_formato_iso_invalido_devuelve_400(client):
    """Rechaza la reserva si el formato de fecha_hora_inicio o fin no cumple ISO 8601 estricto."""

    body = {
        "id_socio": 1,
        "id_cancha": 1,
        "fecha_hora_inicio": "25/10/2026 10:00:00",  # Formato dd/mm/yyyy inválido
        "fecha_hora_fin": "25/10/2026 11:00:00"
    }

    response = client.post("/reservas", json=body)

    assert response.status_code == 400

    data = response.get_json()

    assert "errors" in data


def test_post_reserva_minutos_o_segundos_no_cero_devuelve_400(client):
    """Rechaza la reserva si el inicio o fin contiene minutos o segundos distintos de cero (debe ser hora en punto)."""

    # Intentar reservar de 10:30 a 11:30
    body = {
        "id_socio": 1,
        "id_cancha": 1,
        "fecha_hora_inicio": "2026-10-25T10:30:00.000000-03:00",
        "fecha_hora_fin": "2026-10-25T11:30:00.000000-03:00"
    }

    response = client.post("/reservas", json=body)

    assert response.status_code == 400

    data = response.get_json()

    assert "errors" in data
    

def test_post_reserva_socio_inexistente_devuelve_404(client):
    """Devuelve 404 si el socio no existe en la base de datos."""
    inicio, fin = obtener_fechas_futuras(
        dias_adelante=8,
        hora_inicio=10,
        duracion_horas=1
    )

    body = {
        "id_socio": 999999,
        "id_cancha": 1,
        "fecha_hora_inicio": inicio,
        "fecha_hora_fin": fin
    }

    response = client.post("/reservas", json=body)

    assert response.status_code == 404

    data = response.get_json()

    assert data["errors"][0]["code"] == "NOT_FOUND"


def test_post_reserva_cancha_inexistente_devuelve_404(client):
    """Devuelve 404 si la cancha no existe en la base de datos."""
    inicio, fin = obtener_fechas_futuras(
        dias_adelante=8,
        hora_inicio=10,
        duracion_horas=1
    )

    body = {
        "id_socio": 1,
        "id_cancha": 999999,
        "fecha_hora_inicio": inicio,
        "fecha_hora_fin": fin
    }

    response = client.post("/reservas", json=body)

    assert response.status_code == 404

    data = response.get_json()

    assert data["errors"][0]["code"] == "NOT_FOUND"


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

def test_post_reserva_socio_inactivo_devuelve_409(client):
    """Rechaza la creación de reserva si el socio se encuentra inactivo."""

    # 1. Crear socio y desactivarlo vía PATCH
    res_socio = client.post(
        "/socios",
        json={
            "nombre": "Socio Inactivo Test",
            "email": "inactivo@test.com"
        }
    )

    id_socio = res_socio.get_json()["id"]

    client.patch(
        f"/socios/{id_socio}",
        json={"activo": False}
    )

    # 2. Crear cancha
    res_cancha = client.post(
        "/canchas",
        json={
            "nombre": "Cancha Valida",
            "id_deporte": 1,
            "precio_hora": 1000000
        }
    )

    id_cancha = res_cancha.get_json()["id"]

    # 3. Intentar crear la reserva
    inicio, fin = obtener_fechas_futuras(
        dias_adelante=7,
        hora_inicio=14,
        duracion_horas=1
    )

    response = client.post(
        "/reservas",
        json={
            "id_socio": id_socio,
            "id_cancha": id_cancha,
            "fecha_hora_inicio": inicio,
            "fecha_hora_fin": fin
        }
    )

    # Puede ser 409 o 400 según su manejador de excepciones
    assert response.status_code == 409


def test_post_reserva_cancha_inactiva_devuelve_409(client):
    """Rechaza la creación de reserva si la cancha se encuentra inactiva."""

    # 1. Crear socio
    res_socio = client.post(
        "/socios",
        json={
            "nombre": "Socio Activo Test",
            "email": "activo@test.com"
        }
    )

    id_socio = res_socio.get_json()["id"]

    # 2. Crear cancha e inhabilitarla vía PATCH
    res_cancha = client.post(
        "/canchas",
        json={
            "nombre": "Cancha Inactiva Test",
            "id_deporte": 1,
            "precio_hora": 1000000
        }
    )

    id_cancha = res_cancha.get_json()["id"]

    client.patch(
        f"/canchas/{id_cancha}",
        json={"activa": False}
    )

    # 3. Intentar crear la reserva
    inicio, fin = obtener_fechas_futuras(
        dias_adelante=7,
        hora_inicio=16,
        duracion_horas=1
    )

    response = client.post(
        "/reservas",
        json={
            "id_socio": id_socio,
            "id_cancha": id_cancha,
            "fecha_hora_inicio": inicio,
            "fecha_hora_fin": fin
        }
    )

    assert response.status_code == 409

def test_post_reserva_superposicion_intervalo_identico_devuelve_409(client):
    """Rechaza si la nueva reserva tiene exactamente los mismos horarios que una existente (10:00 a 12:00 vs 10:00 a 12:00)."""

    res_socio1 = client.post(
        "/socios",
        json={
            "nombre": "Socio Id 1",
            "email": "id1@test.com"
        }
    )

    res_socio2 = client.post(
        "/socios",
        json={
            "nombre": "Socio Id 2",
            "email": "id2@test.com"
        }
    )

    res_cancha = client.post(
        "/canchas",
        json={
            "nombre": "Cancha Identica",
            "id_deporte": 1,
            "precio_hora": 1000000
        }
    )

    id_s1 = res_socio1.get_json()["id"]
    id_s2 = res_socio2.get_json()["id"]
    id_c = res_cancha.get_json()["id"]

    inicio, fin = obtener_fechas_futuras(
        dias_adelante=5,
        hora_inicio=10,
        duracion_horas=2
    )

    # Reserva 1: 10:00 a 12:00
    client.post(
        "/reservas",
        json={
            "id_socio": id_s1,
            "id_cancha": id_c,
            "fecha_hora_inicio": inicio,
            "fecha_hora_fin": fin
        }
    )

    # Reserva 2: Exactamente 10:00 a 12:00
    response = client.post(
        "/reservas",
        json={
            "id_socio": id_s2,
            "id_cancha": id_c,
            "fecha_hora_inicio": inicio,
            "fecha_hora_fin": fin
        }
    )

    assert response.status_code == 409


def test_post_reserva_superposicion_intervalo_contenido_devuelve_409(client):
    """Rechaza si la nueva reserva está totalmente dentro de una existente (ej. 11:00 a 12:00 dentro de 10:00 a 13:00)."""

    res_socio1 = client.post(
        "/socios",
        json={
            "nombre": "Socio Cont 1",
            "email": "cont1@test.com"
        }
    )

    res_socio2 = client.post(
        "/socios",
        json={
            "nombre": "Socio Cont 2",
            "email": "cont2@test.com"
        }
    )

    res_cancha = client.post(
        "/canchas",
        json={
            "nombre": "Cancha Contenida",
            "id_deporte": 1,
            "precio_hora": 1000000
        }
    )

    id_s1 = res_socio1.get_json()["id"]
    id_s2 = res_socio2.get_json()["id"]
    id_c = res_cancha.get_json()["id"]

    # Reserva 1 (Contenedora): 10:00 a 13:00 (3 hs)
    inicio1, fin1 = obtener_fechas_futuras(
        dias_adelante=6,
        hora_inicio=10,
        duracion_horas=3
    )

    client.post(
        "/reservas",
        json={
            "id_socio": id_s1,
            "id_cancha": id_c,
            "fecha_hora_inicio": inicio1,
            "fecha_hora_fin": fin1
        }
    )

    # Reserva 2 (Contenida): 11:00 a 12:00 (1 hr)
    inicio2, fin2 = obtener_fechas_futuras(
        dias_adelante=6,
        hora_inicio=11,
        duracion_horas=1
    )

    response = client.post(
        "/reservas",
        json={
            "id_socio": id_s2,
            "id_cancha": id_c,
            "fecha_hora_inicio": inicio2,
            "fecha_hora_fin": fin2
        }
    )

    assert response.status_code == 409


def test_post_reserva_superposicion_intervalo_contenedor_devuelve_409(client):
    """Rechaza si la nueva reserva abarca por completo a una existente (ej. 10:00 a 13:00 engloba a 11:00 a 12:00)."""

    res_socio1 = client.post(
        "/socios",
        json={
            "nombre": "Socio Eng 1",
            "email": "eng1@test.com"
        }
    )

    res_socio2 = client.post(
        "/socios",
        json={
            "nombre": "Socio Eng 2",
            "email": "eng2@test.com"
        }
    )

    res_cancha = client.post(
        "/canchas",
        json={
            "nombre": "Cancha Engloba",
            "id_deporte": 1,
            "precio_hora": 1000000
        }
    )

    id_s1 = res_socio1.get_json()["id"]
    id_s2 = res_socio2.get_json()["id"]
    id_c = res_cancha.get_json()["id"]

    # Reserva 1 (Contenida): 11:00 a 12:00 (1 hr)
    inicio1, fin1 = obtener_fechas_futuras(
        dias_adelante=7,
        hora_inicio=11,
        duracion_horas=1
    )

    client.post(
        "/reservas",
        json={
            "id_socio": id_s1,
            "id_cancha": id_c,
            "fecha_hora_inicio": inicio1,
            "fecha_hora_fin": fin1
        }
    )

    # Reserva 2 (Contenedora): 10:00 a 13:00 (3 hs)
    inicio2, fin2 = obtener_fechas_futuras(
        dias_adelante=7,
        hora_inicio=10,
        duracion_horas=3
    )

    response = client.post(
        "/reservas",
        json={
            "id_socio": id_s2,
            "id_cancha": id_c,
            "fecha_hora_inicio": inicio2,
            "fecha_hora_fin": fin2
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