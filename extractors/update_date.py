"""
Extract and normalise article update dates.

The source website includes update dates in a sentence such as:

    "This article was updated on 12th July 2026"

This module extracts the date portion and converts ordinal dates
(e.g. "12th") into a simpler format ("12") for consistent storage
and comparison.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bs4 import BeautifulSoup


def normalise_date(date_string: str) -> str:
    """
    Remove ordinal suffixes from a date string.

    Converts dates such as:

        "1st July 2026"
        "22nd August 2026"
        "3rd September 2026"

    into:

        "1 July 2026"
        "22 August 2026"
        "3 September 2026"

    Args:
        date_string:
            Date string containing a day, month and year.

    Returns:
        Normalised date string, or the original input if the format
        is not recognised.
    """

    parts = date_string.split()

    if len(parts) != 3:
        return date_string

    day = re.sub(
        r"\D",
        "",
        parts[0]
    )

    return f"{day} {parts[1]} {parts[2]}"


def extract_update_date(soup) -> str | None:
    """
    Extract the article update date from page content.

    Searches the article text for the phrase:

        "This article was updated on"

    and extracts the following date.

    Args:
        soup:
            Parsed article HTML as a BeautifulSoup object.

    Returns:
        Normalised update date if found, otherwise None.
    """

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