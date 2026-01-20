from __future__ import annotations

import os
from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    # Intentionally insecure defaults (training app), but loaded via env like real apps.
    app.secret_key = os.getenv("SECRET_KEY", "super-secret-key-that-should-be-leaked-later")

    # Register routes (kept as same URLs for compatibility with existing templates).
    from .routes import bp as routes_bp

    app.register_blueprint(routes_bp)
    return app

