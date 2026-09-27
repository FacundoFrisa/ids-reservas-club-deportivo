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