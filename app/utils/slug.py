import re
from app.models.card import Card


def make_unique_slug(base: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")
    candidate = slug
    i = 1
    while Card.query.filter_by(slug=candidate).first():
        candidate = f"{slug}-{i}"
        i += 1
    return candidate
