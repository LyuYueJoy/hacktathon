from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# temporary in-memory storage — fine for a hackathon, no DB needed
users = []

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_user = {
            "name": request.form.get("name"),
            "role": request.form.get("role"),
            "ward": request.form.get("ward"),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
        }
        users.append(new_user)
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        for user in users:
            if user["email"] == email and check_password_hash(user["password"], password):
                session["user_name"] = user["name"]
                session["user_role"] = user["role"]
                session["user_ward"] = user["ward"]
                return redirect(url_for("home.home"))

        return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))