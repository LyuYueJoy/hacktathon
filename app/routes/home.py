from flask import Blueprint, render_template
from app.storage import get_tasks

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    tasks = get_tasks()
    return render_template(
        "home.html",
        tasks=tasks,
        total_tasks=len(tasks),
        in_progress_tasks=sum(task.get("status") == "in_progress" for task in tasks),
        completed_tasks=sum(task.get("status") == "completed" for task in tasks),
    )
