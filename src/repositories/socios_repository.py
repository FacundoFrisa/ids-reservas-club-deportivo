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

    @staticmethod
    def existe_email(email):
        conexion = get_db_connection()

        try:
            with conexion.cursor() as cursor:
                query = "SELECT 1 FROM socios WHERE LOWER(email) = LOWER(%s)"
                cursor.execute(query, (email,))

                return cursor.fetchone() is not None

        finally:
            conexion.close()

    @staticmethod
    def crear_socio(nombre, email):
        conexion = get_db_connection()

        try:
            with conexion.cursor() as cursor:
                query = """
                    INSERT INTO socios (nombre, email, activo)
                    VALUES (%s, %s, 1)
                """
                cursor.execute(query, (nombre, email))

                id_nuevo = cursor.lastrowid

                conexion.commit()

                return {
                    "id": id_nuevo,
                    "nombre": nombre,
                    "email": email,
                    "activo": True,
                }

        finally:
            conexion.close()

    @staticmethod
    def existe_email_otro_socio(email, id_socio):
        conexion = get_db_connection()

        try:
            with conexion.cursor() as cursor:
                query = """
                    SELECT 1
                    FROM socios
                    WHERE LOWER(email) = LOWER(%s)
                    AND id != %s
                """
                cursor.execute(query, (email, id_socio))

                return cursor.fetchone() is not None

        finally:
            conexion.close()

    @staticmethod
    def actualizar_socio(id_socio, datos):
        conexion = get_db_connection()

        try:
            with conexion.cursor() as cursor:
                campos_sql = []
                valores = []

                if "nombre" in datos:
                    campos_sql.append("nombre = %s")
                    valores.append(datos["nombre"])

                if "email" in datos:
                    campos_sql.append("email = %s")
                    valores.append(datos["email"])

                if "activo" in datos:
                    campos_sql.append("activo = %s")
                    valores.append(datos["activo"])

                valores.append(id_socio)

                set_sql = ", ".join(campos_sql)

                query = f"""
                    UPDATE socios
                    SET {set_sql}
                    WHERE id = %s
                """

                cursor.execute(query, tuple(valores))

                conexion.commit()

                cursor.execute(
                    """
                    SELECT id, nombre, email, activo
                    FROM socios
                    WHERE id = %s
                    """,
                    (id_socio,),
                )

                socio_actualizado = cursor.fetchone()

                if socio_actualizado:
                    socio_actualizado["activo"] = bool(
                        socio_actualizado["activo"]
                    )

                return socio_actualizado

        finally:
            conexion.close()