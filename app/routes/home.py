from flask import Blueprint, render_template, session
from app.storage import get_patients, get_tasks

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    tasks = get_tasks()
    patients = get_patients()
    current_user = session.get("user_name", "Guest")
    def patient_nurses(patient):
        nurses = patient.get("nurses")
        if isinstance(nurses, list):
            return nurses
        owner = patient.get("owner")
        return [owner] if owner else []

    my_patients = [patient for patient in patients if current_user in patient_nurses(patient)]
    my_tasks = [
        task for task in tasks
        if task.get("assigned_to") == current_user
        or task.get("added_by") == current_user
        or task.get("patient_owner") == current_user
    ]
    return render_template(
        "home.html",
        tasks=tasks,
        my_tasks=my_tasks,
        current_user=current_user,
        patients=patients,
        my_patients=my_patients,
        total_tasks=len(my_patients),
        in_progress_tasks=sum(str(patient.get("status", "Pending")).lower().replace(" ", "_") == "in_progress" for patient in my_patients),
        completed_tasks=sum(str(patient.get("status", "Pending")).lower() == "completed" for patient in my_patients),
    )
