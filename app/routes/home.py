from flask import Blueprint, render_template
from app.routes.task import tasks

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    sorted_tasks = sorted(tasks, key=lambda t: int(t["urgency"]), reverse=True)
    return render_template("home.html", tasks=sorted_tasks, total_tasks=len(tasks))