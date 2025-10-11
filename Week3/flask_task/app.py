from flask import Flask, jsonify
from flasgger import Swagger
from app.routes import api_v1

app = Flask(__name__)

# Swagger configuration
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
    "info": {
        "title": "Task Management API",
        "description": "A simple Flask API demonstrating CRUD operations with Swagger UI (v1).",
        "version": "1.0.0"
    }
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

app.register_blueprint(api_v1)


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400


if __name__ == "__main__":
    app.run(debug=True)
