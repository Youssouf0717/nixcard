from app import db
from sqlalchemy.dialects.sqlite import JSON


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)

    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50))
    email = db.Column(db.String(120))
    job_title = db.Column(db.String(120))
    company = db.Column(db.String(120))
    photo_url = db.Column(db.String(500))

    socials = db.Column(JSON, default={})
    views = db.Column(db.Integer, default=0)
    qr_path = db.Column(db.String(200))
    template = db.Column(db.String(50), default='business')
    accent_color = db.Column(db.String(20), default='#ff6a00')

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
