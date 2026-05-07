

from .auth import auth_bp
from .dashboard import dashboard_bp
from .public import public_bp
from .vcard import vcard_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(vcard_bp)