from flask import Blueprint, request, jsonify, make_response
from app.models.task import Task
from app import db
from datetime import datetime, timezone
import requests
import os


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.get("")
def get_tasks():
    sort_order = request.args.get("sort")
    query = Task.query

    if sort_order == "asc":
        query = query.order_by(Task.title)
    if sort_order == "desc":
        query = query.order_by(Task.title.desc())
    
    tasks = query.all()
    tasks_response = [ task.to_dict() for task in tasks ]
    return tasks_response


@tasks_bp.patch("/<int:task_id>/mark_complete")
def mark_complete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({"error": f"Task {task_id} not found"}), 404
    
    if task.completed_at is None:
        task.completed_at = datetime.now(timezone.utc)
        db.session.commit()
    
    slack_token = os.environ.get("SLACK_TOKEN")
    channel = os.environ.get("SLACK_CHANNEL", "task-notifications")
    text = f"Flora just completed the task *{task.title}*"
    
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {slack_token}"},
        json={"channel": channel, "text": text}
    )

    if not response.ok or response.json().get("ok") is not True:
        print("Slack notification failed:", response.text)
    
    return "", 204


@tasks_bp.patch("/<int:task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({"error": f"Task {task_id} not found"}), 404

    # 只要把 completed_at 设为 None 就是“未完成”
    task.completed_at = None
    db.session.commit()
    return "", 204