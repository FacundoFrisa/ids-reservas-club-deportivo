from src.database.connection import get_db_connection


class ReservasRepository:

    @staticmethod
    def buscar_reservas(filtros, limit, offset):
        conexion = get_db_connection()

        try:
            with conexion.cursor() as cursor:

                where_clauses = []
                params = []

                if "id_cancha" in filtros:
                    where_clauses.append("id_cancha = %s")
                    params.append(filtros["id_cancha"])

                if "id_socio" in filtros:
                    where_clauses.append("id_socio = %s")
                    params.append(filtros["id_socio"])

                if "estado" in filtros:
                    where_clauses.append("estado = %s")
                    params.append(filtros["estado"])

                if "fecha_desde" in filtros:
                    where_clauses.append(
                        "DATE(fecha_hora_inicio) >= %s"
                    )
                    params.append(filtros["fecha_desde"])

                if "fecha_hasta" in filtros:
                    where_clauses.append(
                        "DATE(fecha_hora_inicio) <= %s"
                    )
                    params.append(filtros["fecha_hasta"])

                where_sql = ""

                if where_clauses:
                    where_sql = "WHERE " + " AND ".join(where_clauses)

                query_count = f"""
                    SELECT COUNT(*) AS total
                    FROM reservas
                    {where_sql}
                """

                cursor.execute(query_count, tuple(params))
                total_records = cursor.fetchone()["total"]

                query_data = f"""
                    SELECT
                        id,
                        id_socio,
                        id_cancha,
                        fecha_hora_inicio,
                        fecha_hora_fin,
                        estado,
                        precio_hora,
                        precio_total
                    FROM reservas
                    {where_sql}
                    ORDER BY id ASC
                    LIMIT %s OFFSET %s
                """

                cursor.execute(
                    query_data,
                    tuple(params) + (limit, offset)
                )

                reservas = cursor.fetchall()

                return reservas, total_records

        finally:
            conexion.close()
            
    @staticmethod
    def obtener_reserva_por_id(id_reserva):
        conexion = get_db_connection()

        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        id,
                        id_socio,
                        id_cancha,
                        fecha_hora_inicio,
                        fecha_hora_fin,
                        estado,
                        precio_hora,
                        precio_total
                    FROM reservas
                    WHERE id = %s
                """, (id_reserva,))
                return cursor.fetchone()
        finally:
            conexion.close()