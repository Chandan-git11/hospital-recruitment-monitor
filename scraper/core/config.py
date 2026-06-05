import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
LOG_DIR = DATA_DIR / "logs"
EXPORT_DIR = DATA_DIR / "exports"

DATABASE_PATH = Path(os.getenv("DATABASE_PATH", DATA_DIR / "jobs.db"))
SCRAPER_LOG = Path(os.getenv("SCRAPER_LOG", LOG_DIR / "scraper.log"))
HOSPITALS_FILE = Path(os.getenv("HOSPITALS_FILE", DATA_DIR / "hospitals.json"))
USER_AGENT = os.getenv("USER_AGENT", "HospitalCareerMonitor/1.0")
SCRAPER_INTERVAL_MINUTES = int(os.getenv("SCRAPER_INTERVAL_MINUTES", "60"))
FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "0") in ("1", "true", "True")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
