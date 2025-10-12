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


def create_app():
    app = Flask(__name__)
    CORS(app)

    # === Configuration ===
    app.config["SECRET_KEY"] = "supersecret123"         
    app.config["JWT_SECRET_KEY"] = "jwtsecretkey123"    
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"

    # === JWT Setup ===
    JWTManager(app)

    # === Logging Setup ===
    if not os.path.exists("logs"):
        os.mkdir("logs")

    file_handler = RotatingFileHandler("logs/app.log", maxBytes=10240, backupCount=5)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] in %(module)s: %(message)s"
    )
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Flask App Initialized") 

    # === Error Handling ===
    @app.errorhandler(JWTExtendedException)
    def handle_jwt_error(e):
        app.logger.warning(f"JWT Error: {e}")
        return jsonify({"error": str(e)}), 401

    # === Register Blueprints ===
    app.register_blueprint(auth_bp)   
    app.register_blueprint(api_v1)    

    # === Swagger Configuration ===
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_v1',
                "route": '/api/v1/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Task Management API",
            "description": "Flask API demonstrating CRUD operations with JWT Auth and Swagger UI (v1).",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Enter: **Bearer <JWT Token>**"
            }
        }
    }

    Swagger(app, config=swagger_config, template=swagger_template)
    return app
