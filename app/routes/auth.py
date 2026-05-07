import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, limiter
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

_PWD_RE = re.compile(r'^(?=.*[A-Z])(?=.*\d).{8,}$')


def _validate_password(password: str) -> str | None:
    if len(password) < 8:
        return "Le mot de passe doit contenir au moins 8 caractères."
    if not any(c.isupper() for c in password):
        return "Le mot de passe doit contenir au moins une lettre majuscule."
    if not any(c.isdigit() for c in password):
        return "Le mot de passe doit contenir au moins un chiffre."
    return None


@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not email or not password:
            flash("L'email et le mot de passe sont obligatoires.", "error")
            return redirect(url_for("auth.register"))
        err = _validate_password(password)
        if err:
            flash(err, "error")
            return redirect(url_for("auth.register"))
        if User.query.filter_by(email=email).first():
            flash("Cet email est déjà utilisé.", "error")
            return redirect(url_for("auth.register"))
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("dashboard.index"))
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user and user.is_locked():
            flash("Compte temporairement bloqué suite à plusieurs tentatives. Réessayez dans 15 minutes.", "error")
            return redirect(url_for("auth.login"))

        if not user or not user.check_password(password):
            if user:
                user.record_failed()
                remaining = max(0, 5 - (user.failed_attempts or 0))
                if remaining > 0:
                    flash(f"Mot de passe incorrect. {remaining} tentative(s) restante(s) avant blocage.", "error")
                else:
                    flash("Compte bloqué 15 minutes suite à trop de tentatives.", "error")
            else:
                flash("Email ou mot de passe incorrect.", "error")
            return redirect(url_for("auth.login"))

        user.record_success()
        login_user(user)
        next_page = request.form.get("next") or request.args.get("next")
        if next_page and next_page.startswith("/"):
            return redirect(next_page)
        return redirect(url_for("dashboard.index"))
    return render_template("login.html", next=request.args.get("next", ""))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
