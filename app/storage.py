"""Simple JSON storage used while the hackathon app is small."""

import json
from pathlib import Path
from threading import Lock

DATA_FILE = Path(__file__).parent / "data" / "store.json"
PATIENTS_FILE = Path(__file__).parent / "data" / "patients.json"
_lock = Lock()
_EMPTY_DATA = {"users": [], "tasks": []}


def _read():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text(json.dumps(_EMPTY_DATA, indent=2), encoding="utf-8")
    with DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)
    data.setdefault("users", [])
    data.setdefault("tasks", [])
    return data


def _write(data):
    DATA_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def get_users():
    with _lock:
        return _read()["users"]


def get_patients():
    if not PATIENTS_FILE.exists():
        return []
    with PATIENTS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def add_patient(patient):
    with _lock:
        patients = get_patients()
        patient = dict(patient)
        numeric_ids = [
            int(str(item.get("id", "")).split("-")[-1])
            for item in patients
            if str(item.get("id", "")).split("-")[-1].isdigit()
        ]
        patient["id"] = f"P-{max(numeric_ids, default=0) + 1:03d}"
        patients.append(patient)
        PATIENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        PATIENTS_FILE.write_text(
            json.dumps(patients, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return patient


def get_patient(patient_id):
    return next((patient for patient in get_patients() if str(patient.get("id")) == str(patient_id)), None)


def update_patient(patient_id, changes):
    patients = get_patients()
    for patient in patients:
        if str(patient.get("id")) == str(patient_id):
            patient.update(changes)
            PATIENTS_FILE.write_text(json.dumps(patients, indent=2, ensure_ascii=False), encoding="utf-8")
            return patient
    return None


def delete_patient(patient_id):
    patients = get_patients()
    remaining = [patient for patient in patients if str(patient.get("id")) != str(patient_id)]
    if len(remaining) == len(patients):
        return False
    PATIENTS_FILE.write_text(json.dumps(remaining, indent=2, ensure_ascii=False), encoding="utf-8")
    return True


def delete_tasks_for_patient(patient_id):
    with _lock:
        data = _read()
        data["tasks"] = [task for task in data["tasks"] if str(task.get("patient_id")) != str(patient_id)]
        _write(data)


def find_user_by_email(email):
    normalized_email = email.strip().lower()
    return next(
        (user for user in get_users() if user["email"].lower() == normalized_email),
        None,
    )


def add_user(name, role, ward, email, password):
    with _lock:
        data = _read()
        user = {
            "id": max((user.get("id", 0) for user in data["users"]), default=0) + 1,
            "name": name,
            "role": role,
            "ward": ward,
            "email": email.strip().lower(),
            "password": password,
        }
        data["users"].append(user)
        _write(data)
        return user


def get_tasks():
    with _lock:
        return _read()["tasks"]


def get_task(task_id):
    with _lock:
        return next((task for task in _read()["tasks"] if task.get("id") == task_id), None)


def add_task(task):
    with _lock:
        data = _read()
        task = dict(task)
        task["id"] = max((item.get("id", 0) for item in data["tasks"]), default=0) + 1
        data["tasks"].append(task)
        _write(data)
        return task


def update_task(task_id, changes):
    with _lock:
        data = _read()
        for task in data["tasks"]:
            if task.get("id") == task_id:
                task.update(changes)
                _write(data)
                return task
    return None


def delete_task(task_id):
    with _lock:
        data = _read()
        remaining = [task for task in data["tasks"] if task.get("id") != task_id]
        if len(remaining) == len(data["tasks"]):
            return False
        data["tasks"] = remaining
        _write(data)
        return True
