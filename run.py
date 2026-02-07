"""Entry point to run the Flask development server or Gunicorn (run:app)."""

import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Never run with debug in production; use PORT from environment (e.g. Render)
    is_production = os.environ.get("FLASK_ENV") == "production" or os.environ.get("PRODUCTION")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=not is_production)
