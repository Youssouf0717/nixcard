# Digital Business Cards (Flask MVP)

A scalable MVP SaaS for digital business cards with permanent QR codes.

## Stack
- Flask (modular blueprints + service layer)
- SQLAlchemy (SQLite by default, swap to Postgres via `DATABASE_URL`)
- Flask-Login + Werkzeug password hashing
- `qrcode` for QR generation
- Mobile-first HTML/CSS

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

Open http://localhost:5000

## Project structure

```
app/
├── __init__.py          # App factory, db, login manager
├── models/              # SQLAlchemy models (User, Card)
├── routes/              # Blueprints: auth, dashboard, public
├── services/            # Business logic: card_service, qr_service
├── templates/           # Jinja2 templates
├── static/
│   ├── css/style.css
│   ├── qr/              # Generated QR PNGs
│   └── uploads/         # (reserved for future uploads)
└── utils/               # slug helper, decorators
```

## Scaling later
- **Postgres**: set `DATABASE_URL=postgresql+psycopg://user:pass@host/db` — no code changes.
- **Cloud storage**: `qr_service.py` and any upload code use a single storage abstraction — swap local FS for S3/GCS in one place.
- **Paid plans**: `User.plan` already exists; add a `plans` table + middleware.
- **Analytics**: add a `card_views` table; increment in the `public.show_card` route.
- **Custom domains**: serve `/card/<slug>` from a wildcard domain handler.
- **QR stability**: QR encodes ONLY the public URL — edits to card content never invalidate the code.
