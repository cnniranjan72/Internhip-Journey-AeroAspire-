from flask import Blueprint, jsonify, request
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
        examples:
          application/json: [{"id": 1, "title": "Buy milk", "completed": false}]
    """
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


@api_v1.route("/tasks", methods=["POST"])
def add_task():
    """
    Create a new task
    ---
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
              description: The title of the task
            description:
              type: string
              description: Optional description
    responses:
      201:
        description: Task created successfully
        examples:
          application/json: {"id": 1, "title": "Study", "completed": false}
      400:
        description: Invalid input
    """
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


@api_v1.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """
    Update an existing task
    ---
    parameters:
      - in: path
        name: task_id
        type: integer
        required: true
        description: ID of the task to update
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
            return jsonify(t), 200
    return jsonify({"error": "Task not found"}), 404


@api_v1.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """
    Delete a task
    ---
    parameters:
      - in: path
        name: task_id
        type: integer
        required: true
        description: ID of the task to delete
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
            return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Task not found"}), 404
