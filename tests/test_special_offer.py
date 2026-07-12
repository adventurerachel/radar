"""
Tests for special offer extraction.

These tests verify that the special offer extractor correctly identifies
highlighted promotional text from article HTML.

The extractor relies on both:
    - The expected CSS class used for highlighted offers
    - Text beginning with "SPECIAL OFFER"

The tests use small HTML snippets rather than live webpages so that
they remain fast, reliable, and independent of external websites.

Covered behaviours:
    - Extracting valid special offers
    - Returning None when no offer exists
    - Handling different capitalisation of the offer label
    - Ignoring text with unrelated CSS classes
"""

from bs4 import BeautifulSoup

from extractors.special_offer import extract_special_offer


def test_extracts_special_offer():
    """
    Extract the highlighted special offer text from a valid element.
    """

    html = """
    <p class="has-vivid-red-color">
        SPECIAL OFFER: Earn 50,000 Avios
    </p>
    """

    soup = BeautifulSoup(html, "html.parser")

    result = extract_special_offer(soup)

    assert result == "SPECIAL OFFER: Earn 50,000 Avios"


def test_returns_none_when_no_special_offer():
    """
    Return None when no highlighted special offer exists.
    """

    html = """
    <p>
        No special offer here
    </p>
    """

    soup = BeautifulSoup(html, "html.parser")

    result = extract_special_offer(soup)

    assert result is None

def test_extracts_lowercase_special_offer():
    """
    Handle offer labels with different capitalisation.
    """

    html = """
    <p class="has-vivid-red-color">
        Special Offer: Bonus points available
    </p>
    """

    soup = BeautifulSoup(html, "html.parser")

    result = extract_special_offer(soup)

    assert result == "Special Offer: Bonus points available"

def test_ignores_wrong_css_class():
    """
    Ignore promotional text that does not use the expected CSS class.
    """

    html = """
    <p class="has-black-color">
        SPECIAL OFFER: Something interesting
    </p>
    """

    soup = BeautifulSoup(html, "html.parser")

    result = extract_special_offer(soup)

    assert result is None