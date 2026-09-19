from flask import Blueprint, jsonify, request

from src.services.socios_service import (
    obtener_socios,
    obtener_socio_por_id,
)

from src.utils.pagination import (
    generate_hateoas_links,
    get_pagination_params,
)

from src.validators.socios_validator import (
    validar_id_socio,
    validar_y_obtener_filtros_socios,
)


socios_bp = Blueprint("socios", __name__)


@socios_bp.route("/socios", methods=["GET"])
def get_socios():
    limit, offset = get_pagination_params()

    filtros = validar_y_obtener_filtros_socios(request.args)

    socios, total_records = obtener_socios(
        filtros,
        limit,
        offset
    )

    if not socios:
        return "", 204

    links = generate_hateoas_links(
        request.base_url,
        limit,
        offset,
        total_records,
        request.args
    )

    return jsonify({
        "socios": socios,
        "_links": links
    }), 200


@socios_bp.route("/socios/<int(signed=True):id>", methods=["GET"])
def get_socio_by_id(id):
    validar_id_socio(id)
    socio = obtener_socio_por_id(id)
    return jsonify(socio), 200