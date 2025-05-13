from flask import Blueprint, request, jsonify, make_response
from app.models.goal import Goal
from app.models.task import Task
from app import db

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def get_goal_or_404(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return {"message": f"goal {goal_id} not found"}, 404
    return goal

@goals_bp.post("")
def create_goal():
    try:
        goal = Goal.from_dict(request.get_json())
    except ValueError:
        return {"details": "Invalid data"}, 400

    db.session.add(goal)
    db.session.commit()
    return jsonify({"goal": goal.to_dict()}), 201

# 2) Read all Goals
@goals_bp.get("")
def read_goals():
    goals = Goal.query.all()
    return jsonify([ g.to_dict() for g in goals ]), 200

# 3) Read one Goal
@goals_bp.get("/<int:goal_id>")
def read_one_goal(goal_id):
    goal = get_goal_or_404(goal_id)
    if isinstance(goal, tuple):
        return goal
    return jsonify({"goal": goal.to_dict()}), 200

# 4) Update Goal
@goals_bp.put("/<int:goal_id>")
def update_goal(goal_id):
    goal = get_goal_or_404(goal_id)
    if isinstance(goal, tuple):
        return goal

    data = request.get_json()
    title = data.get("title")
    if title is None:
        return {"details": "Invalid data"}, 400

    goal.title = title
    db.session.commit()
    return "", 204

# 5) Delete Goal
@goals_bp.delete("/<int:goal_id>")
def delete_goal(goal_id):
    goal = get_goal_or_404(goal_id)
    if isinstance(goal, tuple):
        return goal

    db.session.delete(goal)
    db.session.commit()
    return "", 204


# POST /goals/<goal_id>/tasks：
@goals_bp.post("/<int:goal_id>/tasks")
def assign_tasks_to_goal(goal_id):
    goal = get_goal_or_404(goal_id)
    if isinstance(goal, tuple):
        return goal

    task_ids = request.get_json().get("task_ids")
    if task_ids is None or not isinstance(task_ids, list):
        return {"details": "Invalid data"}, 400
    
    tasks = []
    for t_id in task_ids:
        task = Task.query.get(t_id)
        if task is None:
            return {"message": f"Task {t_id} not found"}, 404
        tasks.append(task)

    for task in tasks:
        task.goal = goal

    db.session.commit()

    return jsonify({
        "id": goal.id,
        "task_ids": [ t.id for t in goal.tasks ]
    }), 200


# GET /goals/<goal_id>/tasks
@goals_bp.get("/<int:goal_id>/tasks")
def read_tasks_of_goal(goal_id):
    goal = get_goal_or_404(goal_id)
    if isinstance(goal, tuple):
        return goal

    tasks_list = []
    for task in goal.tasks:
        d = task.to_dict()
        d["goal_id"] = goal.id
        tasks_list.append(d)

    return jsonify({
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_list
    }), 200
