import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))


def test_dashboard_backend_imports_app():
    from dashboard.backend.app import app

    assert app is not None
    assert "api" in app.blueprints
