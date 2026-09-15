from flask import Blueprint, jsonify
from src.services.deportes_service import obtener_todos_los_deportes

deportes_bp = Blueprint("deportes", __name__)

@deportes_bp.route("/deportes", methods=["GET"])
def get_deportes():
    try:
        deportes = obtener_todos_los_deportes()
        
        if not deportes:
            return "", 204
            
        return jsonify({"deportes": deportes}), 200

    except Exception as e:
        return jsonify({
            "errors": [{
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Error al consultar los deportes.",
                "level": "error",
                "description": str(e)
            }]
        }), 500