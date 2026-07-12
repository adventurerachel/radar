"""
Tests for radar alert message formatting.

These tests verify that extracted monitor data is converted into
clear notification messages suitable for sending through Pushover.

The tests focus on message content rather than exact formatting,
allowing minor presentation changes without making the tests brittle.

Covered behaviours:
    - Formatting Barclaycard bonus information
    - Including special offer details
    - Including article update dates
    - Including HSBC conclusion text
    - Generating valid messages when optional data is missing
"""

from alerts.formatter import format_alert_message


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