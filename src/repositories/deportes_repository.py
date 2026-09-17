from src.database.connection import get_db_connection

class DeportesRepository:

    @staticmethod
    def obtener_todos():
        conexion = get_db_connection()

        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id, nombre FROM deportes ORDER BY id ASC")
                return cursor.fetchall()
        finally:
            conexion.close()