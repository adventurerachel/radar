from bs4 import BeautifulSoup

from extractors.special_offer import extract_special_offer


def test_extracts_special_offer():

    html = """
    <p class="has-vivid-red-color">
        SPECIAL OFFER: Earn 50,000 Avios
    </p>
    """

    soup = BeautifulSoup(html, "html.parser")

    result = extract_special_offer(soup)

    assert result == "SPECIAL OFFER: Earn 50,000 Avios"


def test_returns_none_when_no_special_offer():

    html = """
    <p>
        No special offer here
    </p>
    """

    soup = BeautifulSoup(html, "html.parser")

    result = extract_special_offer(soup)

    assert result is None

def test_extracts_lowercase_special_offer():

    html = """
    <p class="has-vivid-red-color">
        Special Offer: Bonus points available
    </p>
    """

    soup = BeautifulSoup(html, "html.parser")

    result = extract_special_offer(soup)

    assert result == "Special Offer: Bonus points available"

def test_ignores_wrong_css_class():

    html = """
    <p class="has-black-color">
        SPECIAL OFFER: Something interesting
    </p>
    """

    soup = BeautifulSoup(html, "html.parser")

    result = extract_special_offer(soup)

    assert result is None