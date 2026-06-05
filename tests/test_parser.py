from scraper.parsers.generic_parser import DefaultParser


def test_default_parser_returns_list():
    parser = DefaultParser()
    result = parser.parse("<html></html>", "apollo")
    assert isinstance(result, list)
    assert result == []
