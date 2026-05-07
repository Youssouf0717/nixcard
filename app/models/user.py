from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    plan = db.Column(db.String(20), default="free")
    failed_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)
    cards = db.relationship("Card", backref="owner", lazy=True)

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def is_locked(self) -> bool:
        if self.locked_until and datetime.now(timezone.utc) < self.locked_until.replace(tzinfo=timezone.utc):
            return True
        return False

    def record_failed(self) -> None:
        self.failed_attempts = (self.failed_attempts or 0) + 1
        if self.failed_attempts >= 5:
            from datetime import timedelta
            self.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
        db.session.commit()

    def record_success(self) -> None:
        self.failed_attempts = 0
        self.locked_until = None
        db.session.commit()
