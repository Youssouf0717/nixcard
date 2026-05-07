"""Authorization helpers."""
from functools import wraps
from flask import abort, g
from flask_login import current_user
from app.models.card import Card


def owns_card(view):
    """Ensure current user owns the card identified by <int:card_id>.
    Returns 403 if not, 404 if missing. Attaches card to flask.g.card.
    """
    @wraps(view)
    def wrapper(card_id, *args, **kwargs):
        card = Card.query.get_or_404(card_id)
        if not current_user.is_authenticated or card.user_id != current_user.id:
            abort(403)
        g.card = card
        return view(card_id, *args, **kwargs)
    return wrapper
