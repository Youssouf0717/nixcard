from flask import Blueprint, render_template
from app.models.card import Card
from app import db

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    return render_template("home.html")


@public_bp.route("/card/<slug>")
def public_card(slug):
    card = Card.query.filter_by(slug=slug).first_or_404()
    card.views = (card.views or 0) + 1
    db.session.commit()
    return render_template("public_card.html", card=card)


@public_bp.route("/animations")
def animations():
    return render_template("animations.html")
