import os
from app import create_app, db  # Added ', db' here

app = create_app()

# THIS FIXES THE 'INTERNAL SERVER ERROR'
# It creates your database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    # Use PORT from environment (e.g. Render) or default to 5000
    is_production = os.environ.get("FLASK_ENV") == "production" or os.environ.get("PRODUCTION")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=not is_production)
