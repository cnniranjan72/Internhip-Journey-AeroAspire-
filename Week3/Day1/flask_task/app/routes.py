from flask import Blueprint, jsonify, request

routes = Blueprint("routes", __name__)   

tasks = []
task_id = 1

@routes.route("/")
def hello():
    return "Hello, World!I am Niranjan C N"

@routes.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@routes.route("/tasks", methods=["POST"])
def add_task():
    global task_id
    data = request.get_json()
    new_task = {
        "id": task_id,
        "title": data.get("title"),
        "description": data.get("description")
    }
    tasks.append(new_task)
    task_id += 1
    return jsonify(new_task), 201
