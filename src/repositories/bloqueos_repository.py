from src.database.connection import get_db_connection


class BloqueosRepository:

    @staticmethod
    def obtener_bloqueos(filtros, limit, offset):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                where_clauses = []
                params = []

                if "id_cancha" in filtros and filtros["id_cancha"]:
                    where_clauses.append("id_cancha = %s")
                    params.append(filtros["id_cancha"])

                if "fecha" in filtros and filtros["fecha"]:
                    where_clauses.append("fecha = %s")
                    params.append(filtros["fecha"])

                where_sql = ""
                if where_clauses:
                    where_sql = "WHERE " + " AND ".join(where_clauses)

                query_count = f"SELECT COUNT(*) AS total FROM bloqueos {where_sql}"
                cursor.execute(query_count, tuple(params))
                total_records = cursor.fetchone()["total"]

                query_data = f"""
                    SELECT id, id_cancha, fecha, hora_inicio, hora_fin, motivo
                    FROM bloqueos
                    {where_sql}
                    ORDER BY id ASC
                    LIMIT %s OFFSET %s
                """
                cursor.execute(query_data, tuple(params) + (limit, offset))
                bloqueos = cursor.fetchall()

                return bloqueos, total_records
        finally:
            conexion.close()

    @staticmethod
    def crear_bloqueo(datos):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                query = """
                    INSERT INTO bloqueos (id_cancha, fecha, hora_inicio, hora_fin, motivo)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    datos['id_cancha'],
                    datos['fecha'],
                    datos['hora_inicio'],
                    datos['hora_fin'],
                    datos.get('motivo')
                ))
                conexion.commit()
                return cursor.lastrowid
        finally:
            conexion.close()

    @staticmethod
    def eliminar_bloqueo(bloqueo_id):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM bloqueos WHERE id = %s", (bloqueo_id,))
                conexion.commit()
                return cursor.rowcount > 0
        finally:
            conexion.close()
    

    @staticmethod
    def existe_superposicion(id_cancha, fecha, hora_inicio, hora_fin):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
               
                query_bloqueos = """
                    SELECT id FROM bloqueos 
                    WHERE id_cancha = %s 
                      AND fecha = %s 
                      AND hora_inicio < %s 
                      AND hora_fin > %s
                """
                cursor.execute(query_bloqueos, (id_cancha, fecha, hora_fin, hora_inicio))
                hay_bloqueo = cursor.fetchone() is not None

                fh_inicio_str = f"{fecha}T{hora_inicio}.000000-03:00"
                fh_fin_str = f"{fecha}T{hora_fin}.000000-03:00"

                query_reservas = """
                    SELECT id FROM reservas 
                    WHERE id_cancha = %s 
                      AND estado = 'confirmada'
                      AND fecha_hora_inicio < %s 
                      AND fecha_hora_fin > %s
                """
                cursor.execute(query_reservas, (id_cancha, fh_fin_str, fh_inicio_str))
                hay_reserva = cursor.fetchone() is not None

                return hay_bloqueo or hay_reserva
        finally:
            conexion.close()