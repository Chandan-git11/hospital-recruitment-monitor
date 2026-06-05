from scraper.services.fetcher import HttpFetcher


def test_http_fetcher_handles_invalid_url(monkeypatch):
    class DummyResponse:
        def raise_for_status(self):
            raise Exception("failed")

    class DummySession:
        def __init__(self, *args, **kwargs):
            self.headers = {}

        def get(self, url, timeout=None, headers=None):
            return DummyResponse()

        def mount(self, *args, **kwargs):
            return None

    monkeypatch.setattr("scraper.services.fetcher.requests.Session", lambda: DummySession())
    fetcher = HttpFetcher()

    assert fetcher.fetch("https://example.invalid") is None
