from flask import Blueprint, render_template, session
from app.storage import get_tasks

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    tasks = get_tasks()
    current_user = session.get("user_name", "Jane Smith")
    my_tasks = [task for task in tasks if task.get("assigned_to") == current_user]
    unassigned_tasks = [task for task in tasks if task.get("assigned_to") in (None, "", "Anyone")]

    sorted_my_tasks = sorted(my_tasks, key=lambda t: int(t["urgency"]), reverse=True)
    sorted_unassigned_tasks = sorted(unassigned_tasks, key=lambda t: int(t["urgency"]), reverse=True)
    sorted_all_tasks = sorted(tasks, key=lambda t: int(t["urgency"]), reverse=True)

    return render_template(
        "home.html",
        tasks=tasks,
        my_tasks=sorted_my_tasks,
        unassigned_tasks=sorted_unassigned_tasks,
        all_tasks=sorted_all_tasks,
        total_tasks=len(tasks),
        in_progress_tasks=sum(task.get("status") == "in_progress" for task in tasks),
        completed_tasks=sum(task.get("status") == "completed" for task in tasks),
        current_user=current_user,
    )
