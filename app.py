from flask import Flask, jsonify
from config import Config
from src.utils.error_handlers import register_error_handlers
from src.routes.deportes_routes import deportes_bp
from src.routes.canchas_routes import canchas_bp
from src.routes.socios_routes import socios_bp

app = Flask(__name__)
register_error_handlers(app)
app.json.ensure_ascii = False
app.json.sort_keys = False

app.register_blueprint(deportes_bp)
app.register_blueprint(canchas_bp)
app.register_blueprint(socios_bp)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "API Club Deportivo funcionando correctamente"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)