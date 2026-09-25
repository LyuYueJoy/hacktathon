from flask import Blueprint, render_template, request

task_bp = Blueprint("task", __name__)

# temporary in-memory storage — fine for a hackathon, no DB needed
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
        }
        tasks.append(new_task)
        print(tasks)  # check your terminal to confirm it worked
        return render_template("task_added.html")  # <-- changed: show confirmation page instead of redirecting

    return render_template("add_task.html")