from flask import Blueprint, jsonify, make_response, request
from src.services import bloqueos_service

bloqueos_bp = Blueprint("bloqueos", __name__)

@bloqueos_bp.route("/bloqueos", methods=["GET"])
def get_bloqueos():

    limit = int(request.args.get('_limit', 10))
    offset = int(request.args.get('_offset', 0))
    
    filtros = {
        "id_cancha": request.args.get('id_cancha'),
        "fecha": request.args.get('fecha')
    }

    bloqueos, total = bloqueos_service.obtener_bloqueos(filtros, limit, offset)
    
    return jsonify({
        "total": total,
        "limit": limit,
        "offset": offset,
        "bloqueos": bloqueos,
        "_links": {}
    }), 200

@bloqueos_bp.route("/bloqueos", methods=["POST"])
def post_bloqueo():
    data = request.get_json(silent=True)
    if not data:
        raise ValueError("El cuerpo de la solicitud no puede estar vacío.")

    nuevo_bloqueo = bloqueos_service.crear_bloqueo(data)
    return jsonify(nuevo_bloqueo), 201

@bloqueos_bp.route("/bloqueos/<int:id>", methods=["DELETE"])
def delete_bloqueo(id):
    bloqueos_service.eliminar_bloqueo(id)
    response = make_response("", 204)
    response.headers["Content-Type"] = "application/json"
    return response