from bs4 import BeautifulSoup

from extractors.update_date import extract_update_date


def test_extracts_article_update_date():

    html = """
    <p>
    This article was updated on 10th July 2026,
    </p>
    """

    soup = BeautifulSoup(html, "html.parser")

    result = extract_update_date(soup)

    assert result == "10 July 2026"