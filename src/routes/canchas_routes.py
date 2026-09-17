from flask import Blueprint, jsonify, request

from src.services.canchas_service import obtener_canchas
from src.validators.canchas_validator import validar_y_obtener_filtros_canchas
from src.utils.pagination import get_pagination_params, generate_hateoas_links

canchas_bp = Blueprint("canchas", __name__)

@canchas_bp.route("/canchas", methods=["GET"])
def get_canchas():
    try:
        limit, offset = get_pagination_params()

        filtros = validar_y_obtener_filtros_canchas(request.args)
        canchas, total_records = obtener_canchas(filtros, limit, offset)

        if not canchas:
            return "", 204

        links = generate_hateoas_links(
            request.base_url,
            limit,
            offset,
            total_records,
            request.args
        )

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