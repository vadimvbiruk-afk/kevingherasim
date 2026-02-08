"""Entry point: start the app. Tables are created in create_app()."""

import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    is_production = os.environ.get("FLASK_ENV") == "production" or os.environ.get("PRODUCTION")
    app.run(host="0.0.0.0", port=port, debug=not is_production)
