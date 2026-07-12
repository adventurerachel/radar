"""
Format radar change notifications.

This module converts extracted article data into a human-readable
message suitable for sending through notification services such as
Pushover.
"""


def format_alert_message(name: str, data: dict) -> str:
    """
    Create a formatted alert message from detected changes.

    The output includes only the fields available in the extracted
    data, allowing different sources to provide different types of
    information.

    Args:
        name:
            Name of the monitored source or article.

        data:
            Dictionary containing extracted change details.

            Supported fields:
                - barclaycard_bonus
                - hsbc_conclusion
                - special_offer
                - update_date

    Returns:
        A formatted multi-line alert message.

    Example:
        Input:
            {
                "special_offer": "Earn 25,000 Avios",
                "update_date": "12 July 2026"
            }

        Output:
            "Barclaycard change detected!

            SPECIAL OFFER:
            Earn 25,000 Avios

            Article updated: 12 July 2026"
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