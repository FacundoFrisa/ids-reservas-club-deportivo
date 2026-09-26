import pytest
from app import app
from src.database.connection import get_db_connection

@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def reset_database():

    conexion = get_db_connection()

    try:
        with conexion.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            cursor.execute("TRUNCATE TABLE reservas;")
            cursor.execute("TRUNCATE TABLE canchas;")
            cursor.execute("TRUNCATE TABLE socios;")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

            conexion.commit()
    finally:
        conexion.close()

    yield


@pytest.fixture
def sample_socio(client):
    res = client.post(
        "/socios",
        json={
            "nombre": "Socio Base Test",
            "email": "socio.base@club.com",
        },
    )

    return res.get_json()


@pytest.fixture
def sample_cancha(client):
    res = client.post(
        "/canchas",
        json={
            "nombre": "Cancha 1 - Fútbol 5 Base",
            "id_deporte": 1,
            "precio_hora": 1000000,
            "techada": False,
            "activa": True,
        },
    )

    return res.get_json()