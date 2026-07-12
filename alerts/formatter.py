"""
Format radar notifications into human-readable messages.

This module contains functions for converting extracted monitor
data into notification messages suitable for Pushover alerts.

Alert types:

    Change alerts:
        Sent when monitored article data differs from the previous
        stored snapshot.

    Special offer alerts:
        Sent whenever an active special offer is detected, even if
        the offer was present during a previous radar run.
"""


def format_alert_message(name: str, data: dict) -> str:
    """
    Format a change detection alert.

    This message is used when monitored article data has changed
    since the previous snapshot.

    Args:
        name:
            Human-readable monitor name.

        data:
            Extracted article data containing any changed fields.

    Returns:
        Formatted alert message containing relevant changed data.

    Example:
        format_alert_message(
            "Barclaycard Avios Plus",
            {
                "barclaycard_bonus": {
                    "bonus_avios": 50000,
                    "spend_requirement_gbp": 3000,
                }
            }
        )
    """

    lines = [
        f"{name} change detected!",
        ""
    ]

    if "barclaycard_bonus" in data:

        bonus = data["barclaycard_bonus"]

        lines.extend([
            f"Bonus: {bonus['bonus_avios']:,} Avios",
            f"Spend requirement: £{bonus['spend_requirement_gbp']:,}",
        ])

    if "hsbc_conclusion" in data:

        lines.extend([
            "Conclusion:",
            data["hsbc_conclusion"],
        ])

    if data.get("special_offer"):

        lines.extend([
            "",
            "SPECIAL OFFER:",
            data["special_offer"],
        ])

    if data.get("update_date"):

        lines.extend([
            "",
            f"Article updated: {data['update_date']}"
        ])

    return "\n".join(lines)

def format_special_offer_alert(name: str, data: dict) -> str:
    """
    Format a recurring special offer notification.

    Unlike change alerts, special offer notifications are generated
    whenever an active special offer exists, regardless of whether
    the offer has changed since the previous run.

    Args:
        name:
            Human-readable monitor name.

        data:
            Extracted article data containing the special offer and
            optional update date.

    Returns:
        Formatted alert message containing the offer details and
        article update date.

    Example:
        format_special_offer_alert(
            "HSBC Premier",
            {
                "special_offer": "Earn 30,000 points",
                "update_date": "1 July 2026"
            }
        )
    """

    lines = [
        f"{name} special offer detected!",
        "",
        "SPECIAL OFFER:",
        data["special_offer"],
    ]

    if data.get("update_date"):
        lines.extend([
            "",
            f"Article updated: {data['update_date']}"
        ])

    return "\n".join(lines)