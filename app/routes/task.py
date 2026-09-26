from flask import Blueprint, render_template, request, session

task_bp = Blueprint("task", __name__)

tasks = []

@task_bp.route("/add-task", methods=["GET", "POST"])
def add_task():
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
        }
        tasks.append(new_task)
        print(tasks)
        return render_template("task_added.html")

    return render_template("add_task.html")