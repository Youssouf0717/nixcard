from flask import Blueprint, Response
from app.models.card import Card

vcard_bp = Blueprint("vcard", __name__)

@vcard_bp.route("/vcard/<slug>")
def vcard(slug):
    card = Card.query.filter_by(slug=slug).first_or_404()

    vcard = f"""BEGIN:VCARD
VERSION:3.0
N:{card.last_name};{card.first_name}
FN:{card.first_name} {card.last_name}
ORG:{card.company or ""}
TITLE:{card.job_title or ""}
TEL:{card.phone or ""}
EMAIL:{card.email or ""}
END:VCARD
"""

    return Response(
        vcard,
        mimetype="text/vcard",
        headers={"Content-Disposition": f"attachment; filename={slug}.vcf"}
    )