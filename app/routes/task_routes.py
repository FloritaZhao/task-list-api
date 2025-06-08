from flask import Blueprint, request, jsonify, make_response
from app.models.task import Task
from app import db
from datetime import datetime, timezone
import requests
import os
from app.routes.utils import validate_model, create_model, get_models_with_filters_and_sort, delete_model

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.get("")
def get_all_tasks():
    return get_models_with_filters_and_sort(Task, request.args)


@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}, 200


@bp.post("")
def create_task():
    request_body = request.get_json()
    return {"task": create_model(Task, request_body)}, 201


@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()
    
    slack_token = os.environ.get("SLACK_TOKEN")
    channel = os.environ.get("SLACK_CHANNEL", "#test-slack-api")
    text = f"Flora just completed the task *{task.title}*"
    
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {slack_token}"},
        json={"channel": channel, "text": text}
    )

    if not response.ok or response.json().get("ok") is not True:
        print("Slack notification failed:", response.text)
    
    return jsonify(None), 204


@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    db.session.commit()
    return jsonify(None), 204


@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    return jsonify(None), 204


@bp.delete("/<int:task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    return delete_model(Task, task_id)
