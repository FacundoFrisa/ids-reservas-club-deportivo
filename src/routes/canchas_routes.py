from flask import Blueprint, jsonify, request
from src.services.canchas_service import obtener_canchas
from src.utils.pagination import get_pagination_params, generate_hateoas_links

canchas_bp = Blueprint("canchas", __name__)

@canchas_bp.route("/canchas", methods=["GET"])
def get_canchas():
    try:
        limit, offset = get_pagination_params()
        if not (1 <= limit <= 100) or offset < 0:
            raise ValueError("El límite debe estar entre 1 y 100, y el offset debe ser mayor o igual a 0.")

        filtros = {}
        if 'id_deporte' in request.args:
            filtros['id_deporte'] = int(request.args.get('id_deporte'))
            
        if 'nombre' in request.args:
            filtros['nombre'] = request.args.get('nombre')
            
        for bool_filter in ['techada', 'activa']:
            if bool_filter in request.args:
                val = request.args.get(bool_filter)
                if val not in ['true', 'false']:
                    raise ValueError(f"El filtro {bool_filter} solo admite 'true' o 'false'.")
                filtros[bool_filter] = val

        canchas, total_records = obtener_canchas(filtros, limit, offset)

        if not canchas:
            return "", 204

        links = generate_hateoas_links(request.base_url, limit, offset, total_records, request.args)
        
        return jsonify({
            "canchas": canchas,
            "_links": links
        }), 200

    except ValueError as ve:

        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "Error de validación en los parámetros.",
                "level": "error",
                "description": str(ve)
            }]
        }), 400
    except Exception as e:

        return jsonify({
            "errors": [{
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Error al consultar las canchas.",
                "level": "error",
                "description": str(e)
            }]
        }), 500