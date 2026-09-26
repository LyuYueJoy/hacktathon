from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.storage import add_user, find_user_by_email

auth_bp = Blueprint("auth", __name__)

# temporary in-memory storage — fine for a hackathon, no DB needed
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        if find_user_by_email(email):
            return render_template("register.html", error="Email is already registered")

        add_user(
            name=request.form.get("name", "").strip(),
            role=request.form.get("role", "").strip(),
            ward=request.form.get("ward", "").strip(),
            email=email,
            password=generate_password_hash(request.form.get("password", "")),
        )
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = find_user_by_email(email)
        if user and check_password_hash(user["password"], password):
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
