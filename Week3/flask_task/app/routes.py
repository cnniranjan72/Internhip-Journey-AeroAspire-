from flask import Blueprint, jsonify, request # type: ignore
from flask_cors import CORS # type: ignore

routes = Blueprint("routes", __name__)

tasks = []
task_id = 1


CORS(routes)

@routes.route("/")
def hello():
    return "Hello, World! I am Niranjan C N"


@routes.route("/tasks", methods=["GET"])
def get_tasks():
    completed = request.args.get("completed")  
    if completed is None:
        return jsonify(tasks)

    if completed.lower() == "true":
        filtered = [t for t in tasks if t.get("completed")]
    elif completed.lower() == "false":
        filtered = [t for t in tasks if not t.get("completed")]
    else:
        return jsonify({"error": "Invalid completed value"}), 400

    return jsonify(filtered)

# POST new task with validation
@routes.route("/tasks", methods=["POST"])
def add_task():
    global task_id
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.get_json()
    title = data.get("title")
    description = data.get("description", "")

    if not title or not isinstance(title, str) or title.strip() == "":
        return jsonify({"error": "Title must be a non-empty string"}), 400

    if description is not None and not isinstance(description, str):
        return jsonify({"error": "Description must be a string"}), 400

    new_task = {
        "id": task_id,
        "title": title.strip(),
        "description": description.strip(),
        "completed": False
    }
    tasks.append(new_task)
    task_id += 1
    return jsonify(new_task), 201


@routes.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    for t in tasks:
        if t["id"] == task_id:
            tasks.remove(t)
            return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Task not found"}), 404

@routes.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.get_json()
    for t in tasks:
        if t["id"] == task_id:
            t["title"] = data.get("title", t["title"])
            t["description"] = data.get("description", t["description"])
            t["completed"] = data.get("completed", t["completed"])
            return jsonify(t), 200
    return jsonify({"error": "Task not found"}), 404
