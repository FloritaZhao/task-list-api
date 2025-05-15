from flask import Blueprint, request, jsonify, make_response
from app.models.goal import Goal
from app.models.task import Task
from app import db
from app.routes.utils import validate_model, create_model, get_models_with_filters


bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@bp.post("")
def create_goal():
    request_body = request.get_json()
    return {"goal": create_model(Goal, request_body)}, 201


@bp.get("")
def read_all_goals():
    return get_models_with_filters(Goal, request.args)


@bp.get("/<goal_id>")
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}, 200


@bp.put("/<goal_id>")
def update_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()
    return "", 204


@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()
    return "", 204


@bp.post("/<goal_id>/tasks")
def assign_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_data = request.get_json()
    task_ids = request_data.get("task_ids")

    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id

    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": task_ids
    }, 200



@bp.get("/<goal_id>/tasks")
def read_tasks_of_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks = [task.to_dict() for task in goal.tasks]
         
    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks
    }, 200
