from datetime import datetime
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
import os
from pathlib import Path

from app.shared.database import init_db
from app.modules.users.routes import users_bp
from app.modules.features.routes import features_bp
from app.modules.votes.routes import votes_bp

load_dotenv()


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///database/db.sqlite"
    )
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")

    # Initialize extensions
    CORS(app)
    JWTManager(app)
    init_db(app)

    # Register health check route
    @app.route("/", methods=["GET"])
    def health_check():
        return {
            "application": "Feature Voting System",
            "status": "running",
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "timestamp": datetime.utcnow().isoformat(),
        }

    # Swagger configuration
    SWAGGER_URL = '/api/docs'
    API_URL = '/swagger.json'
    swagger_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Feature Voting System API"
        }
    )

    # Serve swagger.json
    @app.route('/swagger.json')
    def swagger():
        base_path = Path(__file__).parent.parent
        return send_from_directory(base_path, 'swagger.json')

    # Register blueprints
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(features_bp, url_prefix="/api/features")
    app.register_blueprint(votes_bp, url_prefix="/api/votes")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
