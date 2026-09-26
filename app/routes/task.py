from flask import Blueprint, abort, redirect, render_template, request, session, url_for

from app.storage import (
    add_task as save_task,
    delete_task as remove_task,
    get_task,
    get_users,
    update_task,
)


task_bp = Blueprint("task", __name__)


@task_bp.route("/add-task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        assigned_to = request.form.get("assigned_to", "Anyone") or "Anyone"
        new_task = {
            "name": request.form.get("name"),
            "description": request.form.get("description"),
            "location": request.form.get("location"),
            "notes": request.form.get("notes"),
            "urgency": request.form.get("urgency"),
            "status": "pending",
            "ward": session.get("user_ward"),
            "assigned_to": assigned_to,
            "added_by": session.get("user_name", "Unknown"),
        }
        save_task(new_task)
        return render_template("task_added.html")

    assignees = [user["name"] for user in get_users()] + ["Anyone"]
    return render_template("add_task.html", assignees=assignees)


@task_bp.route("/task/<int:task_id>", methods=["GET"])
def task_detail(task_id):
    task = get_task(task_id)
    if task is None:
        abort(404)
    return render_template("task_detail.html", task=task)


@task_bp.route("/task/<int:task_id>/change-status", methods=["POST"])
def change_status(task_id):
    task = get_task(task_id)
    if task is None:
        abort(404)

    new_status = request.form.get("status")
    if new_status in {"pending", "in_progress", "completed"}:
        update_task(task_id, {"status": new_status})

    return redirect(url_for("home.home"))


@task_bp.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    task = get_task(task_id)
    if task is None:
        abort(404)

    assignees = [user["name"] for user in get_users()] + ["Anyone"]

    if request.method == "POST":
        assigned_to = request.form.get("assigned_to", task.get("assigned_to", "Anyone")) or "Anyone"
        changes = {
            "name": request.form.get("name", task.get("name")),
            "description": request.form.get("description", task.get("description")),
            "location": request.form.get("location", task.get("location")),
            "assigned_to": assigned_to,
            "notes": request.form.get("notes", task.get("notes")),
            "urgency": request.form.get("urgency", task.get("urgency")),
        }
        update_task(task_id, changes)
        return redirect(url_for("home.home"))

    return render_template("edit_task.html", task=task, assignees=assignees)


@task_bp.route("/task/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    if get_task(task_id) is None:
        abort(404)
    remove_task(task_id)
    return redirect(url_for("home.home"))
