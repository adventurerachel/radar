"""
Tests for radar notification formatting.

These tests verify that:

    - change alerts include relevant extracted data
    - special offer alerts include promotion details
    - update dates are included when available
"""

from alerts.formatter import (
    format_alert_message,
    format_special_offer_alert,
)


def test_formats_barclaycard_alert():
    """
    Include Barclaycard bonus and spend requirement details in alerts.
    """

    message = format_alert_message(
        "Barclaycard Avios Plus",
        {
            "barclaycard_bonus": {
                "bonus_avios": 50000,
                "spend_requirement_gbp": 3000,
            }
        }
    )

    assert "Barclaycard Avios Plus change detected!" in message
    assert "Bonus: 50,000 Avios" in message
    assert "Spend requirement: £3,000" in message


def test_formats_special_offer():
    """
    Include special offer text when it is available.
    """

    message = format_alert_message(
        "HSBC",
        {
            "special_offer": "Earn an extra 10,000 points"
        }
    )

    assert "SPECIAL OFFER:" in message
    assert "Earn an extra 10,000 points" in message


def test_formats_update_date():
    """
    Include the article update date when it is available.
    """

    message = format_alert_message(
        "HSBC",
        {
            "update_date": "11 July 2026"
        }
    )

    assert "Article updated: 11 July 2026" in message

def test_formats_hsbc_conclusion():
    """
    Include HSBC conclusion text when available.
    """

    message = format_alert_message(
        "HSBC",
        {
            "hsbc_conclusion": "This card has limited value for Avios collectors."
        }
    )

    assert "Conclusion:" in message
    assert "This card has limited value for Avios collectors." in message

format_alert_message(
    "Test",
    {}
)

def test_formats_special_offer_alert():

    message = format_special_offer_alert(
        "HSBC",
        {
            "special_offer": "SPECIAL OFFER: Earn 30,000 points",
            "update_date": "1 July 2026"
        }
    )

    assert "HSBC special offer detected!" in message
    assert "SPECIAL OFFER:" in message
    assert "Earn 30,000 points" in message
    assert "Article updated: 1 July 2026" in message