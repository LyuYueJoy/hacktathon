from flask import Blueprint, render_template, request, session, redirect, url_for

from app.storage import add_patient, add_task, delete_patient, delete_tasks_for_patient, get_patient, get_users, update_patient


handover_bp = Blueprint("handover", __name__)


def _text(form, name):
    return form.get(name, "").strip()


@handover_bp.route("/new-handover", methods=["GET", "POST"])
def new_handover():
    if request.method == "POST":
        owners = request.form.getlist("nurse_names")
        if not owners and session.get("user_name"):
            owners = [session["user_name"]]

        handover = {
            "room": _text(request.form, "room"),
            "patient": _text(request.form, "patient"),
            "age": _text(request.form, "age"),
            "gender": _text(request.form, "gender"),
            "hospital_id": _text(request.form, "hospital_id"),
            "nurse_role": _text(request.form, "nurse_role"),
            "ward": _text(request.form, "ward"),
            "situation": _text(request.form, "situation"),
            "current_status": _text(request.form, "current_status"),
            "diagnosis": _text(request.form, "diagnosis"),
            "admission_date": _text(request.form, "admission_date"),
            "medical_history": _text(request.form, "medical_history"),
            "context": _text(request.form, "context"),
            "assessment": _text(request.form, "assessment"),
            "findings": _text(request.form, "findings"),
            "recommendation": _text(request.form, "recommendation"),
            "timeline": _text(request.form, "timeline"),
        }

        patient = {
            "room": handover["room"],
            "patient_name": handover["patient"],
            "age": int(handover["age"] or 0),
            "gender": handover["gender"],
            "hospital_id": handover["hospital_id"],
            "ward": handover["ward"],
            "nurses": owners,
            "nurse_name": ", ".join(owners),
            "diagnosis": handover["diagnosis"],
            "status": "Pending",
            "handover": handover,
        }
        patient = add_patient(patient)

        details = (
            f"SITUATION\n{handover['situation']}\n{handover['current_status']}\n\n"
            f"BACKGROUND\n{handover['diagnosis']}\n{handover['medical_history']}\n{handover['context']}\n\n"
            f"ASSESSMENT\n{handover['assessment']}\n{handover['findings']}\n\n"
            f"RECOMMENDATION\n{handover['recommendation']}\n{handover['timeline']}"
        )
        add_task({
            "name": f"HANDOVER — {handover['room']}",
            "patient_name": handover["patient"],
            "nurse_name": ", ".join(owners),
            "patient_owner": owners[0] if owners else "Nurse",
            "patient_id": patient["id"],
            "description": details,
            "location": handover["room"],
            "notes": details,
            "urgency": _text(request.form, "urgency") or "5",
            "status": "pending",
            "assigned_to": owners[0] if owners else "Anyone",
            "added_by": session.get("user_name", "Nurse"),
        })
        return redirect(url_for("home.home"))

    nurses = get_users()
    return render_template("new_handover.html", nurses=nurses)


@handover_bp.route("/patient/<patient_id>/edit", methods=["GET", "POST"])
def edit_patient(patient_id):
    patient = get_patient(patient_id)
    if patient is None:
        return redirect(url_for("home.home"))
    if request.method == "POST":
        owners = request.form.getlist("nurse_names")
        existing_handover = patient.get("handover", {})
        handover_fields = [
            "room", "patient", "age", "gender", "hospital_id", "nurse_role", "ward",
            "situation", "current_status", "diagnosis", "admission_date", "medical_history",
            "context", "assessment", "findings", "recommendation", "timeline",
        ]
        handover = dict(existing_handover)
        for field in handover_fields:
            if field == "patient":
                handover[field] = _text(request.form, "patient_name")
            else:
                handover[field] = _text(request.form, field)

        update_patient(patient_id, {
            "room": _text(request.form, "room"),
            "patient_name": _text(request.form, "patient_name"),
            "age": int(_text(request.form, "age") or 0),
            "gender": _text(request.form, "gender"),
            "hospital_id": _text(request.form, "hospital_id"),
            "ward": _text(request.form, "ward"),
            "diagnosis": _text(request.form, "diagnosis"),
            "nurses": owners or patient.get("nurses", []),
            "nurse_name": ", ".join(owners or patient.get("nurses", [])),
            "handover": handover,
        })
        return redirect(url_for("home.home"))
    return render_template("edit_patient.html", patient=patient, nurses=get_users())


@handover_bp.route("/patient/<patient_id>/status", methods=["POST"])
def change_patient_status(patient_id):
    status = request.form.get("status", "Pending")
    if status not in {"Pending", "In Progress", "Completed"}:
        status = "Pending"
    update_patient(patient_id, {"status": status})
    return redirect(url_for("home.home"))


@handover_bp.route("/patient/<patient_id>/delete", methods=["POST"])
def remove_patient(patient_id):
    delete_patient(patient_id)
    delete_tasks_for_patient(patient_id)
    return redirect(url_for("home.home"))
