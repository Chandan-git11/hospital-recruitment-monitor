import logging
import random
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

MOCK_PAGES_DIR_NAME = "mock_pages"


import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..core.config import USER_AGENT


logger = logging.getLogger("hospital_career_monitor.fetcher")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    USER_AGENT,
]

DEFAULT_TIMEOUT = 15
RETRY_TOTAL = 3
BACKOFF_FACTOR = 1
STATUS_FORCELIST = [429, 500, 502, 503, 504]


def _load_mock_page(file_name: str) -> Optional[str]:
    """Load a local HTML mock page from data/mock_pages/.

    Returns None if the file can't be found.
    """
    try:
        repo_root = Path(__file__).resolve().parents[2]
        mock_path = repo_root / "data" / MOCK_PAGES_DIR_NAME / file_name
        if not mock_path.exists():
            logger.warning("Mock page not found: %s", mock_path)
            return None
        return mock_path.read_text(encoding="utf-8")
    except Exception as exc:
        logger.error("Failed to load mock page %s: %s", file_name, exc)
        return None


class HttpFetcher:
    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        self.timeout = timeout

        self.session = requests.Session()

        self.session.headers.update({"User-Agent": random.choice(USER_AGENTS)})
        retry_strategy = Retry(
            total=RETRY_TOTAL,
            backoff_factor=BACKOFF_FACTOR,
            status_forcelist=STATUS_FORCELIST,
            allowed_methods=["HEAD", "GET", "OPTIONS"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def fetch(self, url: str) -> Optional[str]:
        # If Apollo mock page is available, use it for Apollo career URLs.
        try:
            parsed = urlparse(url)
            host_and_path = f"{parsed.hostname or ''}{parsed.path or ''}".lower()
            if "apollo" in host_and_path:
                return _load_mock_page("apollo.html")
        except Exception as exc:
            logger.debug("Failed to evaluate mock page routing for %s: %s", url, exc)

        headers = {"User-Agent": random.choice(USER_AGENTS)}

        for attempt in range(1, RETRY_TOTAL + 1):
            try:
                logger.debug("Fetching %s attempt %s", url, attempt)
                response = self.session.get(url, timeout=self.timeout, headers=headers)
                response.raise_for_status()
                return response.text
            except requests.RequestException as exc:
                logger.warning("Request failed for %s (attempt %s): %s", url, attempt, exc)
            except Exception as exc:
                logger.error("Unexpected fetch error for %s on attempt %s: %s", url, attempt, exc)

            if attempt < RETRY_TOTAL:
                time.sleep(BACKOFF_FACTOR * attempt)
            else:
                logger.error("Failed to fetch %s after %s attempts", url, attempt)
        return None
