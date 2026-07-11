from bs4 import BeautifulSoup

from extractors.barclaycard import extract_barclaycard_bonus


def test_extracts_barclaycard_bonus_details():

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