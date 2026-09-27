from flask import jsonify
from werkzeug.exceptions import HTTPException
from src.errors.exceptions import APIError

def register_error_handlers(app):

    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = {
            "errors": [
                {
                    "code": error.code,
                    "message": error.message,
                    "level": error.level,
                    "description": error.description
                }
            ]
        }

        return jsonify(response), error.status_code

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        response = {
            "errors": [
                {
                    "code": "BAD_REQUEST",
                    "message": "Error de validación en la solicitud.",
                    "level": "error",
                    "description": str(error)
                }
            ]
        }

        return jsonify(response), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        code_map = {
            400: "BAD_REQUEST",
            404: "NOT_FOUND",
            409: "CONFLICT",
            500: "INTERNAL_SERVER_ERROR"
        }

        response = {
            "errors": [
                {
                    "code": code_map.get(error.code, "HTTP_ERROR"),
                    "message": error.name,
                    "level": "error",
                    "description": error.description
                }
            ]
        }

        return jsonify(response), error.code

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        response = {
            "errors": [
                {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Error interno del servidor.",
                    "level": "error",
                    "description": str(error)
                }
            ]
        }

        return jsonify(response), 500