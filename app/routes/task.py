from flask import Blueprint, render_template

task_bp = Blueprint("task", __name__)


@task_bp.route("/add-task")
def add_task():
    return render_template("add_task.html")