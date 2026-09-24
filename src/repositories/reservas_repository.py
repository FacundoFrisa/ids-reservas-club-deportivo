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
            
    @staticmethod
    def verificar_cancha_y_socio(id_cancha, id_socio):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                # Obtenemos si están activos y el precio vigente de la cancha[cite: 2]
                cursor.execute("SELECT activa, precio_hora FROM canchas WHERE id = %s", (id_cancha,))
                cancha = cursor.fetchone()
                
                cursor.execute("SELECT activo FROM socios WHERE id = %s", (id_socio,))
                socio = cursor.fetchone()
                
                return cancha, socio
        finally:
            conexion.close()

    @staticmethod
    def verificar_superposicion(id_cancha, id_socio, inicio, fin):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                query = """
                    SELECT id, id_cancha, id_socio
                    FROM reservas
                    WHERE estado = 'confirmada'
                      AND (id_cancha = %s OR id_socio = %s)
                      AND fecha_hora_inicio < %s
                      AND fecha_hora_fin > %s
                    LIMIT 1
                """
                cursor.execute(query, (id_cancha, id_socio, fin, inicio))
                return cursor.fetchone()
        finally:
            conexion.close()

    @staticmethod
    def crear_reserva(datos):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                query = """
                    INSERT INTO reservas 
                    (id_socio, id_cancha, fecha_hora_inicio, fecha_hora_fin, estado, precio_hora, precio_total)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    datos['id_socio'], datos['id_cancha'], datos['fecha_hora_inicio'],
                    datos['fecha_hora_fin'], datos['estado'], datos['precio_hora'], datos['precio_total']
                ))
                conexion.commit()
                return cursor.lastrowid
        finally:
            conexion.close()