from src.database.connection import get_db_connection

class CanchasRepository:

    @staticmethod
    def buscar_canchas(filtros, limit, offset):
        conexion = get_db_connection()

        try:
            with conexion.cursor() as cursor:
                query_count = """ SELECT COUNT(*) as total FROM canchas WHERE 1=1 """
                query_data = """ SELECT id, nombre, id_deporte, precio_hora, techada, activa FROM canchas WHERE 1=1 """
                params = []

                if 'id_deporte' in filtros:
                    query_count += " AND id_deporte = %s"
                    query_data += " AND id_deporte = %s"
                    params.append(int(filtros['id_deporte']))
                
                if 'nombre' in filtros:
                    query_count += " AND LOWER(nombre) LIKE LOWER(%s)"
                    query_data += " AND LOWER(nombre) LIKE LOWER(%s)"
                    params.append(f"%{filtros['nombre']}%")

                if 'techada' in filtros:
                    val_techada = 1 if filtros['techada'] == 'true' else 0
                    query_count += " AND techada = %s"
                    query_data += " AND techada = %s"
                    params.append(val_techada)

                if 'activa' in filtros:
                    val_activa = 1 if filtros['activa'] == 'true' else 0
                    query_count += " AND activa = %s"
                    query_data += " AND activa = %s"
                    params.append(val_activa)

                cursor.execute(query_count, tuple(params))
                total_records = cursor.fetchone()['total']

                query_data += " ORDER BY id ASC LIMIT %s OFFSET %s"
                params_data = params + [limit, offset]

                cursor.execute(query_data, tuple(params_data))
                canchas = cursor.fetchall()

                for cancha in canchas:
                    cancha["techada"] = bool(cancha["techada"])
                    cancha["activa"] = bool(cancha["activa"])

                return canchas, total_records

        finally:
            conexion.close()

    @staticmethod
    def crear_cancha(data):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                query = """
                    INSERT INTO canchas (nombre, id_deporte, precio_hora, techada, activa)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    data['nombre'], 
                    data['id_deporte'], 
                    data['precio_hora'], 
                    data['techada'], 
                    data['activa']
                ))
                conexion.commit()

                id_nuevo = cursor.lastrowid

                return {
                    "id": id_nuevo,
                    "nombre": data["nombre"], 
                    "id_deporte": data["id_deporte"], 
                    "precio_hora": data["precio_hora"], 
                    "techada": bool(data["techada"]), 
                    "activa": bool(data["activa"]) 
                }

        finally:
            conexion.close()
            
    @staticmethod
    def obtener_cancha_por_id(id_cancha):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT id, nombre, id_deporte, precio_hora, techada, activa 
                    FROM canchas 
                    WHERE id = %s
                """, (id_cancha,))
                return cursor.fetchone()
        finally:
            conexion.close()

    @staticmethod
    def actualizar_cancha(id_cancha, data):
        if not data:
            return

        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                campos_set = []
                valores = []
                for clave, valor in data.items():
                    campos_set.append(f"{clave} = %s")
                    valores.append(valor)
                
                valores.append(id_cancha)
                query = f"UPDATE canchas SET {', '.join(campos_set)} WHERE id = %s"
                
                cursor.execute(query, tuple(valores))
                conexion.commit()
        finally:
            conexion.close()
            
    @staticmethod
    def tiene_reservas(id_cancha):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT 1 FROM reservas WHERE id_cancha = %s LIMIT 1", (id_cancha,))
                return cursor.fetchone() is not None
        finally:
            conexion.close()

    @staticmethod
    def eliminar_cancha(id_cancha):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM canchas WHERE id = %s", (id_cancha,))
                conexion.commit()
        finally:
            conexion.close()
            
    @staticmethod
    def buscar_canchas_disponibles(filtros, limit, offset):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                base_where = """
                    WHERE c.activa = 1 
                    AND NOT EXISTS (
                        SELECT 1 FROM reservas r 
                        WHERE r.id_cancha = c.id 
                        AND r.estado = 'confirmada' 
                        AND r.fecha_hora_inicio < %s 
                        AND r.fecha_hora_fin > %s
                    )
                """
                
                query_count = f"SELECT COUNT(*) as total FROM canchas c {base_where}"
                query_data = f"SELECT c.id, c.nombre, c.id_deporte, c.precio_hora, c.techada, c.activa FROM canchas c {base_where}"
                
                params = [filtros['fecha_hora_fin'], filtros['fecha_hora_inicio']]

                if 'id_deporte' in filtros:
                    query_count += " AND c.id_deporte = %s"
                    query_data += " AND c.id_deporte = %s"
                    params.append(filtros['id_deporte'])
                
                if 'techada' in filtros:
                    val_techada = 1 if filtros['techada'] == 'true' else 0
                    query_count += " AND c.techada = %s"
                    query_data += " AND c.techada = %s"
                    params.append(val_techada)

                cursor.execute(query_count, tuple(params))
                total_records = cursor.fetchone()['total']

                query_data += " ORDER BY c.id ASC LIMIT %s OFFSET %s"
                params_data = params + [limit, offset]

                cursor.execute(query_data, tuple(params_data))
                canchas = cursor.fetchall()

                return canchas, total_records
        finally:
            conexion.close()