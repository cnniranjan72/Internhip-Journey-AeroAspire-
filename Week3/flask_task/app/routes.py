from flask import Blueprint, jsonify, request

routes = Blueprint("routes", __name__)   

tasks = []
task_id = 1

@routes.route("/")
def hello():
    return "Hello, World!I am Niranjan C N"

@routes.route("/tasks", methods=["GET"])
def get_tasks():
    completed = request.args.get("completed")  # string: "true" / "false" / None
    if completed is None:
        return jsonify(tasks)

    if completed.lower() == "true":
        filtered = [t for t in tasks if t.get("completed")]
    elif completed.lower() == "false":
        filtered = [t for t in tasks if not t.get("completed")]
    else:
        return jsonify({"error": "Invalid completed value"}), 400

    return jsonify(filtered)

@routes.route("/tasks", methods=["POST"])
def add_task():
    global task_id
    data = request.get_json()
    new_task = {
        "id": task_id,
        "title": data.get("title"),
        "description": data.get("description"),
        "completed": False  # new default
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
    data = request.get_json()
    for t in tasks:
        if t["id"] == task_id:
            t["title"] = data.get("title", t["title"])
            t["description"] = data.get("description", t["description"])
            t["completed"] = data.get("completed", t["completed"])
            return jsonify(t), 200
    return jsonify({"error": "Task not found"}), 404
