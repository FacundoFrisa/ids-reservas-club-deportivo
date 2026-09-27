from flask import Blueprint, jsonify, make_response, request
from src.services import bloqueos_service
from src.utils.pagination import get_pagination_params, generate_hateoas_links
from src.validators.bloqueos_validator import validar_y_obtener_filtros_bloqueos, validar_creacion_bloqueo, validar_id_bloqueo

bloqueos_bp = Blueprint("bloqueos", __name__)

@bloqueos_bp.route("/bloqueos", methods=["GET"])
def get_bloqueos():
    limit, offset = get_pagination_params()
    filtros = validar_y_obtener_filtros_bloqueos(request.args)
    bloqueos, total = bloqueos_service.obtener_bloqueos(filtros, limit, offset)

    links = generate_hateoas_links(
        request.base_url,
        limit,
        offset,
        total,
        request.args
    )
    
    return jsonify({
        "bloqueos": bloqueos,
        "_links": links
    }), 200

@bloqueos_bp.route("/bloqueos", methods=["POST"])
def post_bloqueo():
    data = request.get_json(silent=True)
    datos_validados = validar_creacion_bloqueo(data)
    nuevo_bloqueo = bloqueos_service.crear_bloqueo(datos_validados)
    return jsonify(nuevo_bloqueo), 201

@bloqueos_bp.route("/bloqueos/<id>", methods=["DELETE"])
def delete_bloqueo(id):
    id_valido = validar_id_bloqueo(id)
    bloqueos_service.eliminar_bloqueo(id_valido)
    return "", 204