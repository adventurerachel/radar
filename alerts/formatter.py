def format_alert_message(name, data):

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