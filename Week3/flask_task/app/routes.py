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
    Get tasks with filters, search and pagination
    ---
    tags:
      - Tasks
    parameters:
      - in: query
        name: status
        type: string
        required: false
        description: Filter by status (e.g. pending, completed)
      - in: query
        name: completed
        type: string
        required: false
        description: Legacy boolean filter (true/false) - maps to status=completed
      - in: query
        name: search
        type: string
        required: false
        description: Case-insensitive search in title
      - in: query
        name: due_date
        type: string
        required: false
        description: Exact due date filter (YYYY-MM-DD)
      - in: query
        name: page
        type: integer
        required: false
        description: Page number (default 1)
      - in: query
        name: per_page
        type: integer
        required: false
        description: Items per page (default 20)
    responses:
      200:
        description: Paginated list of tasks
    """
    # Read query params
    status = request.args.get("status", type=str)
    completed = request.args.get("completed", type=str)
    search = request.args.get("search", type=str)
    due_date = request.args.get("due_date", type=str)

    # Pagination params with safe defaults
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except (TypeError, ValueError):
        return jsonify({"error": "page and per_page must be integers"}), 400

    if page < 1 or per_page < 1 or per_page > 200:
        return jsonify({"error": "page must be >= 1 and per_page must be between 1 and 200"}), 400

    # Build base query
    query = Task.query

    # completed (legacy) -> map to status
    if completed is not None:
        c = completed.lower()
        if c == "true":
            query = query.filter(Task.status == "completed")
        elif c == "false":
            query = query.filter(Task.status != "completed")
        else:
            return jsonify({"error": "Invalid completed value (use true/false)"}), 400

    # status filter (explicit takes precedence over completed if both provided)
    if status:
        query = query.filter(Task.status == status)

    # due_date filter
    if due_date:
        from datetime import datetime
        try:
            d = datetime.strptime(due_date, "%Y-%m-%d").date()
            query = query.filter(Task.due_date == d)
        except ValueError:
            return jsonify({"error": "Invalid due_date format (use YYYY-MM-DD)"}), 400

    # search by title (case-insensitive)
    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    # Apply ordering (newest first) and paginate
    paginated = query.order_by(Task.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    items = [t.to_dict() for t in paginated.items]
    result = {
        "total": paginated.total,
        "page": paginated.page,
        "per_page": paginated.per_page,
        "pages": paginated.pages,
        "items": items,
    }

    current_app.logger.info(f"Fetched tasks page={page} per_page={per_page} filters={{status:{status}, completed:{completed}, search:{bool(search)}, due_date:{due_date}}}")
    return jsonify(result), 200


@api_v1.route("/tasks", methods=["POST"])
@jwt_required()
def add_task():
    """
    Create a new task (JWT Protected)
    ---
    tags:
      - Tasks
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
        current_app.logger.warning("Task creation failed: Invalid JSON")
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
            return jsonify({"error": "due_date must be in YYYY-MM-DD format"}), 400

    new_task = Task(
        title=title.strip(),
        description=description.strip(),
        status=status,
        due_date=due_date
    )

    db.session.add(new_task)
    db.session.commit()
    current_app.logger.info(f"Task added: {new_task.to_dict()}")
    return jsonify(new_task.to_dict()), 201


@api_v1.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    """
    Update an existing task (JWT Protected)
    ---
    tags:
      - Tasks
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
        current_app.logger.warning(f"Task update failed: ID {task_id} not found")
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
            return jsonify({"error": "due_date must be in YYYY-MM-DD format"}), 400

    db.session.commit()
    current_app.logger.info(f"Task updated: {task.to_dict()}")
    return jsonify(task.to_dict()), 200


@api_v1.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    """
    Delete a task (JWT Protected)
    ---
    tags:
      - Tasks
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
    task = Task.query.get(task_id)
    if not task:
        current_app.logger.warning(f"Task deletion failed: ID {task_id} not found")
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    current_app.logger.info(f"Task deleted: {task_id}")
    return jsonify({"message": "Task deleted"}), 200
