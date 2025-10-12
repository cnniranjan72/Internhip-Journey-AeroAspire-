from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from flask_cors import CORS

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")
CORS(api_v1)

tasks = []
task_id = 1


@api_v1.route("/", methods=["GET"])
def home():
    """
    Root endpoint
    ---
    responses:
      200:
        description: Welcome message
        examples:
          application/json: {"message": "This is API v1"}
    """
    current_app.logger.info("Root endpoint accessed")
    return jsonify({"message": "This is API v1"})


@api_v1.route("/tasks", methods=["GET"])
def get_tasks():
    """
    Get all tasks (optionally filter by completion)
    ---
    parameters:
      - in: query
        name: completed
        type: string
        required: false
        description: Filter tasks by completion status (true/false)
    responses:
      200:
        description: List of tasks
    """
    completed = request.args.get("completed")
    current_app.logger.info(f"Fetching tasks (completed={completed})")

    if completed is None:
        return jsonify(tasks)
    if completed.lower() == "true":
        filtered = [t for t in tasks if t.get("completed")]
    elif completed.lower() == "false":
        filtered = [t for t in tasks if not t.get("completed")]
    else:
        current_app.logger.warning("Invalid filter used for 'completed'")
        return jsonify({"error": "Invalid completed value"}), 400
    return jsonify(filtered)


@api_v1.route("/tasks", methods=["POST"])
@jwt_required()
def add_task():
    """
    Create a new task (JWT Protected)
    ---
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Task
          required:
            - title
          properties:
            title:
              type: string
            description:
              type: string
    responses:
      201:
        description: Task created successfully
      400:
        description: Invalid input
      401:
        description: Unauthorized
    """
    global task_id
    if not request.is_json:
        current_app.logger.warning("Task creation failed: Invalid JSON")
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.get_json()
    title = data.get("title")
    description = data.get("description", "")

    if not title or not isinstance(title, str) or title.strip() == "":
        current_app.logger.warning("Task creation failed: Missing/invalid title")
        return jsonify({"error": "Title must be a non-empty string"}), 400

    if description is not None and not isinstance(description, str):
        current_app.logger.warning("Task creation failed: Invalid description")
        return jsonify({"error": "Description must be a string"}), 400

    new_task = {
        "id": task_id,
        "title": title.strip(),
        "description": description.strip(),
        "completed": False
    }

    tasks.append(new_task)
    current_app.logger.info(f"Task added: {new_task}")
    task_id += 1
    return jsonify(new_task), 201


@api_v1.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    """
    Update an existing task (JWT Protected)
    ---
    security:
      - Bearer: []
    parameters:
      - in: path
        name: task_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          id: TaskUpdate
          properties:
            title:
              type: string
            description:
              type: string
            completed:
              type: boolean
    responses:
      200:
        description: Task updated successfully
      404:
        description: Task not found
    """
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400
    data = request.get_json()

    for t in tasks:
        if t["id"] == task_id:
            t["title"] = data.get("title", t["title"])
            t["description"] = data.get("description", t["description"])
            t["completed"] = data.get("completed", t["completed"])
            current_app.logger.info(f"Task updated: {t}")
            return jsonify(t), 200

    current_app.logger.warning(f"Task update failed: ID {task_id} not found")
    return jsonify({"error": "Task not found"}), 404


@api_v1.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    """
    Delete a task (JWT Protected)
    ---
    security:
      - Bearer: []
    parameters:
      - in: path
        name: task_id
        type: integer
        required: true
    responses:
      200:
        description: Task deleted successfully
      404:
        description: Task not found
    """
    global tasks
    for t in tasks:
        if t["id"] == task_id:
            tasks.remove(t)
            current_app.logger.info(f"Task deleted: {task_id}")
            return jsonify({"message": "Task deleted"}), 200

    current_app.logger.warning(f"Task deletion failed: ID {task_id} not found")
    return jsonify({"error": "Task not found"}), 404
