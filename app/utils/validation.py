"""Validation et normalisation des entrées."""
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[+\d][\d\s\-().]{5,}$")


class ValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def require(value: str | None, field_label: str) -> str:
    v = (value or "").strip()
    if not v:
        raise ValidationError(f"{field_label} est obligatoire.")
    return v


def validate_email(value: str, field_label: str = "Email") -> str:
    v = require(value, field_label)
    if not EMAIL_RE.match(v):
        raise ValidationError(f"{field_label} n'est pas une adresse valide.")
    return v.lower()


def validate_phone(value: str, field_label: str = "Téléphone") -> str:
    v = require(value, field_label)
    if not PHONE_RE.match(v):
        raise ValidationError(f"{field_label} n'est pas un numéro valide.")
    return v


def normalize_url(value: str | None) -> str | None:
    if not value:
        return None
    v = value.strip()
    if not v:
        return None
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.\-]*://", v):
        v = "https://" + v
    return v
