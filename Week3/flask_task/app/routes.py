from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from flask_cors import CORS
from datetime import datetime

from .models import db, Task

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")
CORS(api_v1)


@api_v1.route("/", methods=["GET"])
def home():
    """
    Root Endpoint
    ---
    tags:
      - Root
    responses:
      200:
        description: API v1 welcome message
        examples:
          application/json: {"message": "This is API v1"}
    """
    current_app.logger.info("Root endpoint accessed")
    return jsonify({"message": "This is API v1"})


@api_v1.route("/tasks", methods=["GET"])
def get_tasks():
    """
    Get all tasks with optional filters and pagination
    ---
    tags:
      - Tasks
    parameters:
      - name: status
        in: query
        type: string
        required: false
        description: Filter tasks by status (pending, completed)
      - name: completed
        in: query
        type: string
        required: false
        description: Legacy boolean filter (true/false)
      - name: search
        in: query
        type: string
        required: false
        description: Search in title (case-insensitive)
      - name: due_date
        in: query
        type: string
        required: false
        description: Filter by due date (YYYY-MM-DD)
      - name: page
        in: query
        type: integer
        required: false
        description: Page number (default 1)
      - name: per_page
        in: query
        type: integer
        required: false
        description: Items per page (default 20)
    responses:
      200:
        description: Paginated list of tasks
    """
    status = request.args.get("status")
    completed = request.args.get("completed")
    search = request.args.get("search")
    due_date = request.args.get("due_date")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    if page < 1 or per_page < 1 or per_page > 200:
        return jsonify({"error": "page must be >=1 and per_page must be 1-200"}), 400

    query = Task.query

    if completed:
        c = completed.lower()
        if c == "true":
            query = query.filter(Task.status == "completed")
        elif c == "false":
            query = query.filter(Task.status != "completed")
        else:
            return jsonify({"error": "Invalid completed value"}), 400

    if status:
        query = query.filter(Task.status == status)

    if due_date:
        try:
            d = datetime.strptime(due_date, "%Y-%m-%d").date()
            query = query.filter(Task.due_date == d)
        except ValueError:
            return jsonify({"error": "Invalid due_date format"}), 400

    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    paginated = query.order_by(Task.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    result = {
        "total": paginated.total,
        "page": paginated.page,
        "per_page": paginated.per_page,
        "pages": paginated.pages,
        "items": [t.to_dict() for t in paginated.items],
    }

    return jsonify(result), 200


@api_v1.route("/tasks", methods=["POST"])
@jwt_required()
def add_task():
    """
    Create a new task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
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
            status:
              type: string
            due_date:
              type: string
              format: date
    responses:
      201:
        description: Task created successfully
      400:
        description: Invalid input
      401:
        description: Unauthorized
    """
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.get_json()
    title = data.get("title")
    description = data.get("description", "")
    status = data.get("status", "pending")
    due_date_str = data.get("due_date")

    if not title or title.strip() == "":
        return jsonify({"error": "Title is required"}), 400

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "due_date must be YYYY-MM-DD"}), 400

    new_task = Task(title=title.strip(), description=description.strip(), status=status, due_date=due_date)
    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict()), 201


@api_v1.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    """
    Update a task by ID
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          id: TaskUpdate
          properties:
            title:
              type: string
            description:
              type: string
            status:
              type: string
            due_date:
              type: string
              format: date
    responses:
      200:
        description: Task updated successfully
      404:
        description: Task not found
    """
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.status = data.get("status", task.status)

    due_date_str = data.get("due_date")
    if due_date_str:
        try:
            task.due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "due_date must be YYYY-MM-DD"}), 400

    db.session.commit()
    return jsonify(task.to_dict()), 200


@api_v1.route("/tasks/<int:task_id>/complete", methods=["PATCH"])
@jwt_required()
def mark_complete(task_id):
    """
    Mark a task as completed
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Task marked completed
      404:
        description: Task not found
    """
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    task.status = "completed"
    db.session.commit()
    return jsonify({"message": "Task marked completed", "task": task.to_dict()}), 200


@api_v1.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    """
    Delete a task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Task deleted
      404:
        description: Task not found
    """
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200
