from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Enable cross-origin access, allowing the front-end's local development environment to access the back-end.
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "http://localhost:5174",
                "http://127.0.0.1:5174",
                "http://localhost:3000",
                "https://sunsmart-platform.vercel.app"
            ]
        }
    })

    # Register Router
    from app.routes.uv_routes import uv_bp
    from app.routes.health_routes import health_bp
    from app.routes.weather_routes import weather_bp
    from app.routes.awareness_routes import awareness_bp

    app.register_blueprint(uv_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(awareness_bp)

    return app