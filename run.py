from waitress import serve
from app import app

# Run your Flask app with Waitress
serve(app, host="0.0.0.0", port=5000)
