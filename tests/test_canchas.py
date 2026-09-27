from datetime import datetime, timedelta
from src.utils.time_utils import obtener_fechas_futuras

def test_post_cancha_exito(client):
    body = {
        "nombre": "Cancha Test Pytest",
        "id_deporte": 1,
        "precio_hora": 1200000,
        "techada": True,
    }

    response = client.post("/canchas", json=body)

    assert response.status_code == 201

    data = response.get_json()

    assert data is not None, (
        "El endpoint POST /canchas debe devolver "
        "el objeto JSON creado"
    )
    assert data["nombre"] == "Cancha Test Pytest"
    assert data["techada"] is True


def test_post_cancha_precio_invalido_devuelve_400(client):
    body = {
        "nombre": "Cancha Gratis",
        "id_deporte": 1,
        "precio_hora": 0,
    }

    response = client.post("/canchas", json=body)

    assert response.status_code == 400

    data = response.get_json()

    assert "errors" in data
    assert len(data["errors"]) > 0
    assert data["errors"][0]["code"] == "BAD_REQUEST"

def test_post_cancha_deporte_inexistente_devuelve_404(client):
    body = {
        "nombre": "Cancha Deporte Inexistente",
        "id_deporte": 99999,
        "precio_hora": 1500000,
    }

    response = client.post("/canchas", json=body)

    assert response.status_code == 404

    data = response.get_json()

    assert "errors" in data
    assert len(data["errors"]) > 0
    assert data["errors"][0]["code"] == "NOT_FOUND"


def test_delete_cancha_con_reservas_devuelve_409(client):
    """Rechaza eliminar una cancha que tiene reservas asociadas."""

    # 1. Crear socio
    res_socio = client.post(
        "/socios",
        json={
            "nombre": "Socio Delete Reserva",
            "email": "delete.reserva@test.com"
        }
    )

    assert res_socio.status_code == 201

    id_socio = res_socio.get_json()["id"]

    # 2. Crear cancha
    res_cancha = client.post(
        "/canchas",
        json={
            "nombre": "Cancha Con Reserva",
            "id_deporte": 1,
            "precio_hora": 1000000
        }
    )

    assert res_cancha.status_code == 201

    id_cancha = res_cancha.get_json()["id"]

    # 3. Crear una reserva para la cancha
    inicio, fin = obtener_fechas_futuras(
        dias_adelante=10,
        hora_inicio=10,
        duracion_horas=1
    )

    res_reserva = client.post(
        "/reservas",
        json={
            "id_socio": id_socio,
            "id_cancha": id_cancha,
            "fecha_hora_inicio": inicio,
            "fecha_hora_fin": fin
        }
    )

    assert res_reserva.status_code == 201

    # 4. Intentar eliminar la cancha
    response = client.delete(f"/canchas/{id_cancha}")

    assert response.status_code == 409

    data = response.get_json()

    assert "errors" in data

def test_get_canchas_combinacion_filtros_y_paginacion(client):
    """Verifica que los filtros se combinen correctamente y que se aplique paginación."""

    # Cancha A: cumple todos los filtros
    res_a = client.post(
        "/canchas",
        json={
            "nombre": "Cancha A Techada",
            "id_deporte": 1,
            "precio_hora": 1000000,
            "techada": True,
            "activa": True
        }
    )

    # Cancha B: mismo deporte, pero no techada
    res_b = client.post(
        "/canchas",
        json={
            "nombre": "Cancha B Descubierta",
            "id_deporte": 1,
            "precio_hora": 1000000,
            "techada": False,
            "activa": True
        }
    )

    # Cancha C: techada, pero otro deporte
    res_c = client.post(
        "/canchas",
        json={
            "nombre": "Cancha C Otro Deporte",
            "id_deporte": 2,
            "precio_hora": 1000000,
            "techada": True,
            "activa": True
        }
    )

    # Cancha D: también cumple todos los filtros
    res_d = client.post(
        "/canchas",
        json={
            "nombre": "Cancha D Techada",
            "id_deporte": 1,
            "precio_hora": 1000000,
            "techada": True,
            "activa": True
        }
    )

    assert res_a.status_code == 201
    assert res_b.status_code == 201
    assert res_c.status_code == 201
    assert res_d.status_code == 201

    id_a = res_a.get_json()["id"]
    id_d = res_d.get_json()["id"]

    # Aplicamos múltiples filtros + paginación
    response = client.get(
        "/canchas",
        query_string={
            "id_deporte": 1,
            "techada": "true",
            "activa": "true",
            "_limit": 1,
            "_offset": 0
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "canchas" in data
    assert "_links" in data

    # Solo debe devolver una cancha por _limit=1
    assert len(data["canchas"]) == 1

    # La cancha devuelta debe cumplir los filtros
    cancha = data["canchas"][0]

    assert cancha["id"] in [id_a, id_d]
    assert cancha["id_deporte"] == 1
    assert cancha["techada"] is True
    assert cancha["activa"] is True

    response_offset = client.get(
        "/canchas",
        query_string={
            "id_deporte": 1,
            "techada": "true",
            "activa": "true",
            "_limit": 1,
            "_offset": 1
        }
    )

    assert response_offset.status_code == 200

    data_offset = response_offset.get_json()

    assert len(data_offset["canchas"]) == 1

    cancha_offset = data_offset["canchas"][0]

    assert cancha_offset["id"] in [id_a, id_d]
    assert cancha_offset["id"] != cancha["id"]