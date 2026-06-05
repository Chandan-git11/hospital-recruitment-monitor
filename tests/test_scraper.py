from scraper.utils import load_hospitals


def test_load_hospitals_reads_json():
    hospitals = load_hospitals()
    assert isinstance(hospitals, list)
    assert any(isinstance(item, dict) for item in hospitals)
