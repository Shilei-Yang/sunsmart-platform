"""
Sun Smart Platform - Flask backend server.
Default port 5000. Override with FLASK_PORT in backend/.env (e.g. FLASK_PORT=5001).
"""
import os
from dotenv import load_dotenv
load_dotenv()
from app import create_app

app = create_app()
PORT = int(os.environ.get("FLASK_PORT", 5000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)