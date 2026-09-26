from flask import Blueprint, render_template, request

handover_bp = Blueprint("handover", __name__)


def _handover_from_form(form):
    fields = [
        "room", "patient", "age", "nurse_name", "nurse_role", "ward",
        "gender", "hospital_id", "situation", "current_status", "diagnosis",
        "admission_date", "medical_history", "context", "assessment", "findings",
        "recommendation", "timeline",
    ]
    return {field: form.get(field, "").strip() for field in fields}


@handover_bp.route("/new-handover", methods=["GET", "POST"])
def new_handover():
    if request.method == "POST":
        return render_template("home.html", handover=_handover_from_form(request.form))
    return render_template("new_handover.html")
