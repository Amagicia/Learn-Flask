from waitress import serve
from app import app  # Assuming 'app' is your Flask app instance

if __name__ == "__main__":
    print("Starting server...")
    serve(app, host="0.0.0.0", port=5000)
