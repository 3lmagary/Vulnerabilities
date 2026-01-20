"""
Backward-compatible entrypoint.

The app has a more production-like Flask layout under `vulnapp/` (app factory, blueprints).
Existing usage (`python3 app.py`) still works.
"""

import os

from vulnapp import create_app


app = create_app()


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(host=host, port=port, debug=debug)
