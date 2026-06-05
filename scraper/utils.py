import json
from .core.config import DATA_DIR, EXPORT_DIR, LOG_DIR, HOSPITALS_FILE


def ensure_data_directories() -> None:
    for path in [DATA_DIR, EXPORT_DIR, LOG_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def load_hospitals() -> list[dict]:
    if not HOSPITALS_FILE.exists():
        return []

    with HOSPITALS_FILE.open("r", encoding="utf-8") as handle:
        try:
            return json.load(handle)
        except json.JSONDecodeError:
            return []
