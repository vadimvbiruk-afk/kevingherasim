"""Entry point to run the Flask development server or Gunicorn (run:app)."""

import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Never run with debug in production
    is_production = os.environ.get("FLASK_ENV") == "production" or os.environ.get("PRODUCTION")
    app.run(debug=not is_production)
