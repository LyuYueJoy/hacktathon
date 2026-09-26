from flask import Blueprint, render_template, request, session, redirect, url_for
from app.storage import add_task as save_task, delete_task as remove_task, get_task, get_users, update_task

task_bp = Blueprint("task", __name__)

@task_bp.route("/add-task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        save_task({
            "name": request.form.get("name", "").strip(),
            "description": request.form.get("description", "").strip(),
            "location": request.form.get("location", "").strip(),
            "notes": request.form.get("notes", "").strip(),
            "urgency": request.form.get("urgency", "5"),
            "status": "pending",
            "ward": session.get("user_ward"),
            "assigned_to": request.form.get("assigned_to", "Anyone") or "Anyone",
            "added_by": session.get("user_name", "Unknown"),
        })
        return render_template("task_added.html")
    assignees = [user["name"] for user in get_users()] + ["Anyone"]
    return render_template("add_task.html", assignees=assignees)

@task_bp.route("/task/<int:task_id>/status", methods=["POST"])
def change_status(task_id):
    status = request.form.get("status", "pending")
    if status not in {"pending", "in_progress", "completed"}:
        status = "pending"
    update_task(task_id, {"status": status})
    return redirect(url_for("home.home"))

@task_bp.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    task = get_task(task_id)
    if task is None:
        return redirect(url_for("home.home"))
    if request.method == "POST":
        update_task(task_id, {
            "name": request.form.get("name", "").strip(),
            "description": request.form.get("description", "").strip(),
            "location": request.form.get("location", "").strip(),
            "notes": request.form.get("notes", "").strip(),
            "urgency": request.form.get("urgency", "5"),
            "assigned_to": request.form.get("assigned_to", "Anyone") or "Anyone",
        })
        return redirect(url_for("home.home"))
    assignees = [user["name"] for user in get_users()] + ["Anyone"]
    return render_template("edit_task.html", task=task, assignees=assignees)

@task_bp.route("/task/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    remove_task(task_id)
    return redirect(url_for("home.home"))
