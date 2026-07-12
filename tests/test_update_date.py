"""
Tests for article update date extraction.

These tests verify that the update date extractor correctly identifies
article update notices and converts dates into a consistent format.

The tests use small HTML snippets rather than live webpages so that
they remain fast, reliable, and independent of external websites.

Covered behaviours:
    - Extracting dates from article update text
    - Removing ordinal suffixes from day numbers
    - Returning dates in a consistent format
"""

from bs4 import BeautifulSoup

from extractors.update_date import extract_update_date


def test_extracts_article_update_date():
    """
    Extract and normalise an article update date.
    """

    html = """
    <p>
    This article was updated on 10th July 2026,
    </p>
    """

    soup = BeautifulSoup(html, "html.parser")

    result = extract_update_date(soup)

    assert result == "10 July 2026"

def test_returns_none_when_update_date_not_found():
    """
    Return None when the article does not contain an update notice.
    """

    html = """
    <p>
        This article was originally published in July 2026.
    </p>
    """

    soup = BeautifulSoup(html, "html.parser")

    result = extract_update_date(soup)

    assert result is None

def test_removes_different_ordinal_suffixes():
    """
    Remove ordinal suffixes from different day numbers.
    """

    html = """
    <p>
    This article was updated on 1st July 2026,
    </p>
    """

    soup = BeautifulSoup(html, "html.parser")

    result = extract_update_date(soup)

    assert result == "1 July 2026"