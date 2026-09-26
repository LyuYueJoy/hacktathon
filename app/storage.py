"""Simple JSON storage used while the hackathon app is small."""

import json
from pathlib import Path
from threading import Lock

DATA_FILE = Path(__file__).parent / "data" / "store.json"
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


def add_task(task):
    with _lock:
        data = _read()
        task = dict(task)
        task["id"] = max((item.get("id", 0) for item in data["tasks"]), default=0) + 1
        data["tasks"].append(task)
        _write(data)
        return task
