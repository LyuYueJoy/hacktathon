from flask import Blueprint, render_template, session
from app.routes.task import tasks

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    current_user = session.get("user_name", "Jane Smith")
    my_tasks = [task for task in tasks if task.get("assigned_to") == current_user]
    unassigned_tasks = [task for task in tasks if task.get("assigned_to") in (None, "", "Anyone")]

    sorted_my_tasks = sorted(my_tasks, key=lambda t: int(t["urgency"]), reverse=True)
    sorted_unassigned_tasks = sorted(unassigned_tasks, key=lambda t: int(t["urgency"]), reverse=True)

    return render_template(
        "home.html",
        my_tasks=sorted_my_tasks,
        unassigned_tasks=sorted_unassigned_tasks,
        total_tasks=len(tasks),
        current_user=current_user,
    )