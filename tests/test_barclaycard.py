"""
Tests for Barclaycard bonus extraction.

These tests verify that the Barclaycard extractor correctly identifies
sign-up bonus information from article HTML.

The tests use small HTML snippets rather than live webpages so that
they remain:
    - Fast to run
    - Reliable
    - Independent of external websites

Covered behaviours:
    - Extracting Avios bonus amounts
    - Extracting spend requirements
    - Handling missing bonus sections
    - Finding information across multiple HTML elements
    - Handling headings containing additional text
"""

from bs4 import BeautifulSoup

from extractors.barclaycard import extract_barclaycard_bonus


def test_extracts_barclaycard_bonus_details():
    """
    Extract Avios bonus and spend requirement from a standard article
    section.
    """

    html = """
    <h2>
        What is the Barclaycard Avios Plus Mastercard sign-up bonus?
    </h2>

    <p>
        Earn 50,000 Avios when you apply for the card.
    </p>

    <p>
        You need to spend £3,000 within the required period.
    </p>
    """

    soup = BeautifulSoup(html, "html.parser")

    result = extract_barclaycard_bonus(soup)

    assert result == {
        "bonus_avios": 50000,
        "spend_requirement_gbp": 3000,
    }


def test_returns_none_when_bonus_not_found():
    """
    Return empty values when the expected bonus section does not exist.
    """

    html = """
    <h2>
        Barclaycard Avios Plus Mastercard benefits
    </h2>

    <p>
        Earn rewards on your everyday spending.
    </p>
    """

    soup = BeautifulSoup(html, "html.parser")

    result = extract_barclaycard_bonus(soup)

    assert result == {
        "bonus_avios": None,
        "spend_requirement_gbp": None,
    }


def test_extracts_bonus_across_multiple_elements():
    """
    Extract relevant values even when bonus information is spread
    across different HTML elements.
    """

    html = """
    <h2>
        What is the Barclaycard Avios Plus Mastercard sign-up bonus?
    </h2>

    <p>
        Earn 50,000 Avios.
    </p>

    <h3>
        Eligibility
    </h3>

    <p>
        Spend £3,000 to qualify.
    </p>
    """

    soup = BeautifulSoup(html, "html.parser")

    result = extract_barclaycard_bonus(soup)

    assert result["bonus_avios"] == 50000
    assert result["spend_requirement_gbp"] == 3000


def test_handles_heading_with_extra_text():
    """
    Extract values when the target heading contains additional text.
    """

    html = """
    <h2>
        What is the Barclaycard Avios Plus Mastercard sign-up bonus? Updated guide
    </h2>

    <p>
        Earn 60,000 Avios and spend £4,000.
    </p>
    """

    soup = BeautifulSoup(html, "html.parser")

    result = extract_barclaycard_bonus(soup)

    assert result["bonus_avios"] == 60000
    assert result["spend_requirement_gbp"] == 4000