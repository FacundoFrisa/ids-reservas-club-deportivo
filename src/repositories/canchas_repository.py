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

                return canchas, total_records

        finally:
            conexion.close()