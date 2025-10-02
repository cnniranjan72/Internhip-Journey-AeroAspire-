from flask import Flask, jsonify # type: ignore
from app.routes import routes

app = Flask(__name__)
app.register_blueprint(routes)

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400

if __name__ == "__main__":
    app.run(debug=True)
