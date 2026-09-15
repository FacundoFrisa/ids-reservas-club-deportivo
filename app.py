from flask import Flask, jsonify
from config import Config

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "API Club Deportivo funcionando correctamente"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)