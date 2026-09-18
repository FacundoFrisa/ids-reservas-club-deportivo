from flask import Blueprint, jsonify, request

from src.services.canchas_service import obtener_canchas, crear_cancha
from src.validators.canchas_validator import validar_y_obtener_filtros_canchas, validar_creacion_cancha
from src.utils.pagination import get_pagination_params, generate_hateoas_links

canchas_bp = Blueprint("canchas", __name__)

@canchas_bp.route("/canchas", methods=["GET"])
def get_canchas(): 
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

        
@canchas_bp.route("/canchas", methods=["POST"])
def post_cancha():
    data = request.get_json(silent=True)
    if data is None:
        raise ValueError("El cuerpo de la solicitud debe ser un objeto JSON válido y no estar vacío.")
    
    datos_limpios = validar_creacion_cancha(data)
    crear_cancha(datos_limpios)

    return "", 201