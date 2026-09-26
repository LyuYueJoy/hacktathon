from flask import Blueprint, render_template, request
from app.storage import add_task

handover_bp = Blueprint("handover", __name__)


def _handover_from_form(form):
    fields = [
        "room", "patient", "age", "changed", "watch_out", "waiting_on",
        "next_nurse", "previous_notes", "urgency",
    ]
    return {field: form.get(field, "").strip() for field in fields}


@handover_bp.route("/new-handover", methods=["GET", "POST"])
def new_handover():
    if request.method == "POST":
        handover = _handover_from_form(request.form)
        details = (
            f"Patient: {handover['patient']}, {handover['age']}\n\n"
            f"WHAT CHANGED\n{handover['changed']}\n\n"
            f"WATCH OUT FOR\n{handover['watch_out']}\n\n"
            f"WAITING ON\n{handover['waiting_on']}\n\n"
            f"NEXT NURSE SHOULD KNOW\n{handover['next_nurse']}\n\n"
            f"NOTES FROM PREVIOUS SHIFT\n{handover['previous_notes']}"
        )
        add_task({
            "name": f"HANDOVER — {handover['room']}",
            "description": details,
            "location": handover["room"],
            "notes": details,
            "urgency": handover["urgency"],
            "status": "pending",
            "assigned_to": "Anyone",
            "added_by": "Nurse",
        })
        from flask import redirect, url_for
        return redirect(url_for("home.home"))
    return render_template("new_handover.html")
