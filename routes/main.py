from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from .auth import login_required
from extensions import db
from models import User

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html", username=session.get("username"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=session.get("username"))


@main_bp.route("/profile")
@login_required
def profile():
    user = db.session.get(User, session["user_id"])
    return render_template("profile.html", user=user)


@main_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    user = db.session.get(User, session["user_id"])

    if request.method == "POST":
        current_password = request.form.get("current_password", "").strip()
        new_password = request.form.get("new_password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        if not current_password or not new_password or not confirm_password:
            flash("All fields are required.", "error")
            db.close()
            return redirect(url_for("main.settings"))

        if not check_password_hash(user.password_hash, current_password):
            flash("Current password is incorrect.", "error")
            db.close()
            return redirect(url_for("main.settings"))

        if new_password != confirm_password:
            flash("The new passwords do not match.", "error")
            db.close()
            return redirect(url_for("main.settings"))

        if len(new_password) < 8:
            flash("New password must be at least 8 characters long.", "error")
            db.close()
            return redirect(url_for("main.settings"))

        user.password_hash = generate_password_hash(new_password)
        db.add(user)
        db.commit()
        db.close()

        flash("Your password has been updated.", "success")
        return redirect(url_for("main.settings"))

    return render_template("settings.html", user=user)


@main_bp.route("/docs")
def api_docs():
    return render_template("api_docs.html")
