from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from flask_login import login_required, current_user
from app.services.card_service import create_card, update_card, delete_card as svc_delete
from app.utils.decorators import owns_card
from app.utils.validation import ValidationError
import os

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def index():
    from app.models.card import Card
    cards = Card.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", cards=cards)


@dashboard_bp.route("/dashboard/new", methods=["GET", "POST"])
@login_required
def new_card():
    if request.method == "POST":
        try:
            create_card(current_user.id, request.form, request.files)
            flash("Carte créée avec succès.", "success")
            return redirect(url_for("dashboard.index"))
        except ValidationError as e:
            flash(e.message, "error")
    return render_template("card_form.html")


@dashboard_bp.route("/dashboard/card/<int:card_id>")
@login_required
@owns_card
def card_detail(card_id):
    card = g.card
    base_url = os.getenv("BASE_URL", "http://localhost:5000")
    public_url = f"{base_url}/card/{card.slug}"
    return render_template("card_detail.html", card=card, public_url=public_url, qr_rel=card.qr_path or "")


@dashboard_bp.route("/dashboard/card/<int:card_id>/edit", methods=["GET", "POST"])
@login_required
@owns_card
def edit_card(card_id):
    card = g.card
    if request.method == "POST":
        try:
            update_card(card, request.form, request.files)
            flash("Carte mise à jour.", "success")
            return redirect(url_for("dashboard.card_detail", card_id=card.id))
        except ValidationError as e:
            flash(e.message, "error")
    return render_template("card_form.html", card=card)


@dashboard_bp.route("/dashboard/card/<int:card_id>/delete", methods=["POST"])
@login_required
@owns_card
def delete_card(card_id):
    svc_delete(g.card)
    flash("Carte supprimée.", "success")
    return redirect(url_for("dashboard.index"))
