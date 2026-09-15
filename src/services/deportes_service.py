from src.database.connection import get_db_connection

def obtener_todos_los_deportes():
    conexion = get_db_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre FROM deportes ORDER BY id ASC")
            return cursor.fetchall()
    finally:
        conexion.close()