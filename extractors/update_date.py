import re


def normalise_date(date_string):

    parts = date_string.split()

    if len(parts) != 3:
        return date_string

    day = re.sub(
        r"\D",
        "",
        parts[0]
    )

    return f"{day} {parts[1]} {parts[2]}"


def extract_update_date(soup):

    text = soup.get_text(
        " ",
        strip=True
    )

    match = re.search(
        r"This article was updated on\s+([A-Za-z0-9]+\s+[A-Za-z]+\s+\d{4})",
        text,
        re.IGNORECASE
    )

    if not match:
        return None

    found_date = match.group(1)

    return normalise_date(found_date)