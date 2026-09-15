from flask import Flask, jsonify
from config import Config
from src.routes.deportes_routes import deportes_bp

app = Flask(__name__)
app.json.ensure_ascii = False

app.register_blueprint(deportes_bp)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "API Club Deportivo funcionando correctamente"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)