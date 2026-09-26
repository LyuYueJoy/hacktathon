from flask import Blueprint, request, jsonify, session
from datetime import datetime

chat_bp = Blueprint("chat", __name__)

# temporary in-memory storage — fine for a hackathon, no DB needed
messages = []

@chat_bp.route("/chat/messages", methods=["GET"])
def get_messages():
    return jsonify(messages)

@chat_bp.route("/chat/send", methods=["POST"])
def send_message():
    text = request.form.get("text")
    if text:
        messages.append({
            "user": session.get("user_name", "Anonymous"),
            "text": text,
            "time": datetime.now().strftime("%H:%M"),
        })
    return jsonify(messages)