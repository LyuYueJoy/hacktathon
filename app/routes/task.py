from flask import Blueprint, render_template, request, session, abort
from app.storage import get_tasks, add_task

task_bp = Blueprint("task", __name__)

@task_bp.route("/add-task", methods=["GET", "POST"], endpoint="add_task")
def add_task_view():
    if request.method == "POST":
        new_task = {
            "name": request.form.get("name"),
            "description": request.form.get("description"),
            "location": request.form.get("location"),
            "notes": request.form.get("notes"),
            "urgency": request.form.get("urgency"),
            "status": "pending",
            "ward": session.get("user_ward"),
            "added_by": session.get("user_name", "Unknown"),
            "assigned_to": "Anyone",
        }
        add_task(new_task)
        return render_template("task_added.html")

    return render_template("add_task.html")


@task_bp.route("/task/<int:task_id>")
def task_detail(task_id):
    task = next((t for t in get_tasks() if t.get("id") == task_id), None)
    if task is None:
        abort(404)
    return render_template("task_detail.html", task=task)