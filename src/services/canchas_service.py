from src.database.connection import get_db_connection

def obtener_canchas(filtros, limit, offset):
    conexion = get_db_connection()
    try:
        with conexion.cursor() as cursor:
            query_count = "SELECT COUNT(*) as total FROM canchas WHERE 1=1"
            query_data = "SELECT id, nombre, id_deporte, precio_hora, techada, activa FROM canchas WHERE 1=1"
            params = []
            
            # Filtro: id_deporte
            if 'id_deporte' in filtros:
                query_count += " AND id_deporte = %s"
                query_data += " AND id_deporte = %s"
                params.append(int(filtros['id_deporte']))
                
            # Filtro: nombre
            if 'nombre' in filtros:
                query_count += " AND nombre LIKE %s"
                query_data += " AND nombre LIKE %s"
                params.append(f"%{filtros['nombre']}%")
                
            # Filtro: techada
            if 'techada' in filtros:
                val_techada = 1 if filtros['techada'] == 'true' else 0
                query_count += " AND techada = %s"
                query_data += " AND techada = %s"
                params.append(val_techada)
                
            # Filtro: activa
            if 'activa' in filtros:
                val_activa = 1 if filtros['activa'] == 'true' else 0
                query_count += " AND activa = %s"
                query_data += " AND activa = %s"
                params.append(val_activa)

            cursor.execute(query_count, tuple(params))
            total_records = cursor.fetchone()['total']

            query_data += " ORDER BY id ASC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cursor.execute(query_data, tuple(params))
            canchas = cursor.fetchall()

            for cancha in canchas:
                cancha['techada'] = bool(cancha['techada'])
                cancha['activa'] = bool(cancha['activa'])

            return canchas, total_records
    finally:
        conexion.close()