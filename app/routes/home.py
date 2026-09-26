from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)

SAMPLE_HANDOVER = {
    "room": "Room 12", "patient": "Jane", "age": "67",
    "nurse_name": "Alex Morgan", "nurse_role": "Registered Nurse", "ward": "Medical Ward",
    "gender": "Female", "hospital_id": "HN-20481",
    "situation": "Patient became dizzy after standing.",
    "current_status": "Blood pressure dropped 130/80 → 105/65. New dizziness at 2:30pm.",
    "diagnosis": "Post-operative recovery", "admission_date": "12 September 2026",
    "medical_history": "Hypertension. Penicillin allergy.",
    "context": "Normally independent and alert.",
    "assessment": "Increased fall risk following dizziness on mobilisation.",
    "findings": "Monitor blood pressure. No new skin, line or drain concerns.",
    "recommendation": "Assist when mobilising and review dizziness before walking.",
    "timeline": "Repeat observations in 30 minutes; doctor review this shift.",
}


@home_bp.route("/")
def home():
    return render_template("home.html", handover=SAMPLE_HANDOVER)
