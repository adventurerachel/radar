from alerts.formatter import format_alert_message


def test_formats_barclaycard_alert():

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

    message = format_alert_message(
        "HSBC",
        {
            "special_offer": "Earn an extra 10,000 points"
        }
    )

    assert "SPECIAL OFFER:" in message
    assert "Earn an extra 10,000 points" in message


def test_formats_update_date():

    message = format_alert_message(
        "HSBC",
        {
            "update_date": "11 July 2026"
        }
    )

    assert "Article updated: 11 July 2026" in message