from flask import Blueprint, jsonify, request
from src.services.deportes_service import obtener_todos_los_deportes
from src.validators.deportes_validator import validar_peticion_deportes

deportes_bp = Blueprint("deportes", __name__)

@deportes_bp.route("/deportes", methods=["GET"])
def get_deportes():
    validar_peticion_deportes(request.args)

    deportes = obtener_todos_los_deportes()
    
    if not deportes:
        return "", 204
        
    return jsonify({"deportes": deportes}), 200