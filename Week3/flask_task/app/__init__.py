from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
from flask_jwt_extended.exceptions import JWTExtendedException
import logging
from logging.handlers import RotatingFileHandler
import os

from .routes import api_v1
from .auth import auth_bp
from .models import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    app.config["SECRET_KEY"] = "supersecret123"
    app.config["JWT_SECRET_KEY"] = "jwtsecretkey123"
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    instance_dir = os.path.join(project_root, "instance")
    os.makedirs(instance_dir, exist_ok=True)
    db_path = os.path.join(instance_dir, "tasks.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app, db)
    JWTManager(app)

    logs_dir = os.path.join(project_root, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    file_handler = RotatingFileHandler(os.path.join(logs_dir, "app.log"), maxBytes=10240, backupCount=5)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] in %(module)s: %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Flask App Initialized")

    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to the Task API! Visit /apidocs/ for documentation."})

    @app.errorhandler(JWTExtendedException)
    def handle_jwt_error(e):
        app.logger.warning(f"JWT Error: {e}")
        return jsonify({"error": str(e)}), 401

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error(f"Server error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_v1)

    # Swagger config
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec_v1",
                "route": "/api/v1/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Task Management API",
            "description": "Flask API demonstrating CRUD operations with JWT Auth, Swagger UI, and SQLAlchemy integration (v1).",
            "version": "1.0.0",
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Enter: **Bearer <JWT Token>**",
            }
        },
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    with app.app_context():
        db.create_all()
        app.logger.info("Database tables created or verified.")

    return app
