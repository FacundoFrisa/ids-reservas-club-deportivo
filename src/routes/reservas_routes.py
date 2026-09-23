from flask import Blueprint, jsonify, request

from src.services.reservas_service import obtener_reservas
from src.validators.reservas_validator import validar_y_obtener_filtros_reservas
from src.utils.pagination import get_pagination_params, generate_hateoas_links


reservas_bp = Blueprint("reservas", __name__)


@reservas_bp.route("/reservas", methods=["GET"])
def get_reservas():
    limit, offset = get_pagination_params()

    filtros = validar_y_obtener_filtros_reservas(request.args)

    reservas, total_records = obtener_reservas(
        filtros,
        limit,
        offset
    )

    links = generate_hateoas_links(
        request.base_url,
        limit,
        offset,
        total_records,
        request.args
    )

    return jsonify({
        "reservas": reservas,
        "_links": links
    }), 200