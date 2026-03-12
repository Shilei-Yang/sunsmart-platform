"""
Sun Smart Platform - Flask backend server.
"""
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint for frontend and monitoring."""
    return jsonify({"status": "ok", "message": "Backend is running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
