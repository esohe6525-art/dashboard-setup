from flask import Blueprint, jsonify, request

from extensions import db
from models import Task


tasks_bp = Blueprint("tasks", __name__)


def validate_task_data(data):
    if not data:
        return False, "Request must be JSON."
    if not data.get("title"):
        return False, "Task title is required."
    return True, None


@tasks_bp.route("/tasks", methods=["GET"])
def list_tasks():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks]), 200


@tasks_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({"error": "Task not found."}), 404
    return jsonify(task.to_dict()), 200


@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    valid, error = validate_task_data(data)
    if not valid:
        return jsonify({"error": error}), 400

    task = Task(
        title=data["title"],
        description=data.get("description"),
        completed=bool(data.get("completed", False)),
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@tasks_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({"error": "Task not found."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request must be JSON."}), 400

    if "title" in data:
        task.title = data["title"] or task.title
    if "description" in data:
        task.description = data["description"]
    if "completed" in data:
        task.completed = bool(data["completed"])

    db.session.commit()
    return jsonify(task.to_dict()), 200


@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({"error": "Task not found."}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully."}), 200
