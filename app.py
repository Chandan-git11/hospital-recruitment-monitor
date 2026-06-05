import sys
from pathlib import Path

from flask import Flask
from flask_cors import CORS

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from dashboard.backend.api_routes import api_bp
from scraper.core.config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG

app = Flask(__name__)
CORS(app)
app.register_blueprint(api_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
