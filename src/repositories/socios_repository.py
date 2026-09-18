from src.database.connection import get_db_connection


class SociosRepository:

    @staticmethod
    def obtener_socios(filtros, limit, offset):
        conexion = get_db_connection()

        try:
            with conexion.cursor() as cursor:
                where_clauses = []
                params = []

                if "nombre" in filtros and filtros["nombre"]:
                    where_clauses.append(
                        "LOWER(nombre) LIKE LOWER(%s)"
                    )
                    params.append(f"%{filtros['nombre']}%")

                if "activo" in filtros and filtros["activo"] is not None:
                    where_clauses.append("activo = %s")
                    params.append(filtros["activo"])

                where_sql = ""

                if where_clauses:
                    where_sql = "WHERE " + " AND ".join(where_clauses)

                count_query = f"""
                    SELECT COUNT(*) AS total
                    FROM socios
                    {where_sql}
                """

                cursor.execute(count_query, tuple(params))
                total_records = cursor.fetchone()["total"]

                query = f"""
                    SELECT id, nombre, email, activo
                    FROM socios
                    {where_sql}
                    ORDER BY id ASC
                    LIMIT %s OFFSET %s
                """

                cursor.execute(
                    query,
                    tuple(params) + (limit, offset)
                )

                socios = cursor.fetchall()

                for socio in socios:
                    socio["activo"] = bool(socio["activo"])

                return socios, total_records

        finally:
            conexion.close()

    @staticmethod
    def obtener_socio_por_id(id_socio):
        conexion = get_db_connection()

        try:
            with conexion.cursor() as cursor:
                query = """
                    SELECT id, nombre, email, activo
                    FROM socios
                    WHERE id = %s
                """

                cursor.execute(query, (id_socio,))
                socio = cursor.fetchone()

                if socio:
                    socio["activo"] = bool(socio["activo"])

                return socio

        finally:
            conexion.close()