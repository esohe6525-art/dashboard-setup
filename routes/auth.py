from flask import Blueprint, app, flash, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from models import SessionLocal, User

auth_bp = Blueprint("auth", __name__, template_folder="templates")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Please enter both a username and password.", "error")
            return redirect(url_for("auth.register"))

        session = SessionLocal()
        existing_user = session.query(User).filter(User.username == username).first()
        if existing_user:
            flash("That username is already taken.", "error")
            session.close()
            return redirect(url_for("auth.register"))

        user = User(username=username, password_hash=generate_password_hash(password))
        session.add(user)
        session.commit()
        session.close()

        flash("Account created successfully. You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        session = SessionLocal()
        user = session.query(User).filter(User.username == username).first()
        session.close()

        if user and check_password_hash(user.password_hash, password):
            flash("Login successful", "success")
            return redirect(url_for("main.index"))

        flash("Invalid username or password.", "error")
        return redirect(url_for("auth.login"))

    return render_template("auth/login.html")



