from flask import Flask, jsonify
from config import Config
from src.database.connection import get_db_connection

app = Flask(__name__)
app.json.ensure_ascii = False

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "API Club Deportivo funcionando correctamente"}), 200

@app.route("/deportes", methods=["GET"])
def obtener_deportes():
    try:
        conexion = get_db_connection()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre FROM deportes")
            deportes = cursor.fetchall()
        conexion.close()

        if not deportes:
            return '', 204

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)