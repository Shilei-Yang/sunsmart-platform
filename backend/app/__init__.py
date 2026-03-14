from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(app)

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
        return response

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