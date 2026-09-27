from flask import Blueprint, jsonify, request

from src.services.canchas_service import obtener_canchas, crear_cancha, obtener_cancha_por_id, actualizar_cancha, eliminar_cancha, obtener_canchas_disponibles
from src.validators.canchas_validator import validar_y_obtener_filtros_canchas, validar_creacion_cancha, validar_actualizacion_cancha, validar_id_cancha, validar_y_obtener_filtros_disponibles
from src.utils.pagination import get_pagination_params, generate_hateoas_links
from src.errors.exceptions import BadRequestError

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
    datos_limpios = validar_creacion_cancha(data)
    nueva_cancha = crear_cancha(datos_limpios)
    return jsonify(nueva_cancha), 201

@canchas_bp.route("/canchas/disponibles", methods=["GET"])
def get_canchas_disponibles():
    limit, offset = get_pagination_params()
    filtros = validar_y_obtener_filtros_disponibles(request.args)
    
    canchas, total_records = obtener_canchas_disponibles(filtros, limit, offset)

    links = generate_hateoas_links(
        request.base_url,
        limit,
        offset,
        total_records,
        request.args
    )

    return jsonify({
        "canchas": canchas if canchas else [],
        "_links": links
    }), 200

@canchas_bp.route("/canchas/<id>", methods=["GET"])
def get_cancha_id(id):
    id_valido = validar_id_cancha(id)
    cancha = obtener_cancha_por_id(id_valido)
    return jsonify(cancha), 200

@canchas_bp.route("/canchas/<id>", methods=["PATCH"])
def patch_cancha(id):
    id_valido = validar_id_cancha(id)
    data = request.get_json(silent=True)
    datos_limpios = validar_actualizacion_cancha(data)
    actualizar_cancha(id_valido, datos_limpios)
    return "", 204

@canchas_bp.route("/canchas/<id>", methods=["DELETE"])
def delete_cancha(id):
    id_valido = validar_id_cancha(id)
    eliminar_cancha(id_valido)
    
    return "", 204