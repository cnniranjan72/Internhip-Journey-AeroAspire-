from flask import Flask
from .routes import api_v1

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_v1) 
    return app
