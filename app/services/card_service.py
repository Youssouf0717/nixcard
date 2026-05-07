import os
import uuid
from app import db
from app.models.card import Card
from app.utils.slug import make_unique_slug
from app.utils.validation import (
    require, validate_email, validate_phone, normalize_url, ValidationError,
)
from app.services import qr_service

UPLOAD_FOLDER = os.path.join("app", "static", "uploads")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}
SOCIAL_KEYS = ["whatsapp", "facebook", "instagram", "linkedin", "website"]
URL_SOCIAL_KEYS = {"facebook", "instagram", "linkedin", "website"}


def _save_photo(files) -> str | None:
    if not files:
        return None
    f = files.get("photo")
    if not f or not f.filename:
        return None
    ext = f.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return None
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.{ext}"
    f.save(os.path.join(UPLOAD_FOLDER, filename))
    return f"uploads/{filename}"


def _clean_socials(form) -> dict:
    socials: dict[str, str] = {}
    for key in SOCIAL_KEYS:
        raw = (form.get(f"social_{key}") or "").strip()
        if not raw:
            continue
        if key in URL_SOCIAL_KEYS:
            normalized = normalize_url(raw)
            if normalized:
                socials[key] = normalized
        else:
            socials[key] = raw
    return socials


def _extract_required(form) -> dict:
    return {
        "first_name": require(form.get("first_name"), "Prénom"),
        "last_name": require(form.get("last_name"), "Nom"),
        "phone": validate_phone(form.get("phone"), "Téléphone"),
        "email": validate_email(form.get("email"), "Email"),
    }


VALID_TEMPLATES = {"business", "minimal", "luxury", "creator"}

def _apply_optional(card: Card, form, files=None) -> None:
    card.job_title = (form.get("job_title") or "").strip() or None
    card.company = (form.get("company") or "").strip() or None
    card.socials = _clean_socials(form)
    photo = _save_photo(files)
    if photo:
        card.photo_url = photo
    tpl = (form.get("template") or "business").strip()
    card.template = tpl if tpl in VALID_TEMPLATES else "business"
    import re
    color = (form.get("accent_color") or "#ff6a00").strip()
    card.accent_color = color if re.match(r'^#[0-9a-fA-F]{6}$', color) else "#ff6a00"


def create_card(user_id: int, form, files=None) -> Card:
    data = _extract_required(form)
    slug = make_unique_slug(f"{data['first_name']}-{data['last_name']}")
    card = Card(user_id=user_id, slug=slug, **data)
    _apply_optional(card, form, files)
    db.session.add(card)
    db.session.commit()
    card.qr_path = qr_service.generate_qr(card.slug)
    db.session.commit()
    return card


def update_card(card: Card, form, files=None) -> Card:
    data = _extract_required(form)
    for k, v in data.items():
        setattr(card, k, v)
    _apply_optional(card, form, files)
    db.session.commit()
    return card


def delete_card(card: Card) -> None:
    slug = card.slug
    # Supprime la photo uploadée si locale
    if card.photo_url and card.photo_url.startswith("uploads/"):
        try:
            os.remove(os.path.join("app", "static", card.photo_url))
        except FileNotFoundError:
            pass
    db.session.delete(card)
    db.session.commit()
    qr_service.delete_qr(slug)
