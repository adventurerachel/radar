"""
Extract Barclaycard Avios Plus sign-up bonus details from a Head for Points article.

The extraction logic is intentionally scoped to the section headed:

    "What is the Barclaycard Avios Plus Mastercard sign-up bonus?"

This avoids matching unrelated Avios values that may appear elsewhere
in the article, such as promotional examples, historical offers, or
comparison tables.
"""
from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bs4 import BeautifulSoup

def extract_barclaycard_bonus(soup: BeautifulSoup) -> dict[str, int | None]:
    """
    Extract the current Barclaycard Avios Plus sign-up offer.

    The function locates the article section describing the sign-up
    bonus, then searches the surrounding content for:

    - Bonus Avios awarded
    - Minimum spend requirement in GBP

    Args:
        soup:
            Parsed article HTML as a BeautifulSoup object.

    Returns:
        Dictionary containing:

        - bonus_avios:
            Number of Avios awarded for the sign-up bonus.

        - spend_requirement_gbp:
            Required spend in pounds sterling.

    Example:
        {
            "bonus_avios": 25000,
            "spend_requirement_gbp": 3000,
        }
    """

    elements = soup.find_all(["h2", "h3", "p"])

    paragraphs = [
        element.get_text(" ", strip=True)
        for element in elements
    ]

    bonus_avios = None
    spend_requirement = None

    target_heading = (
        "what is the barclaycard avios plus mastercard sign-up bonus?"
    )

    for index, text in enumerate(paragraphs):

        if target_heading in text.lower().strip():

            # Restrict extraction to the target section and a small
            # number of following elements. This reduces the risk of
            # capturing Avios values from unrelated parts of the article.
            following_text = " ".join(
                paragraphs[index:index + 5]
            )

            # Extract the first Avios amount mentioned in the offer section.
            avios_match = re.search(
                r"([\d,]+)\s+Avios",
                following_text,
                re.IGNORECASE,
            )

            if avios_match:
                bonus_avios = int(
                    avios_match.group(1).replace(",", "")
                )

            spend_match = re.search(
                r"£\s?([\d,]+)",
                following_text,
            )

            if spend_match:
                spend_requirement = int(
                    spend_match.group(1).replace(",", "")
                )

            break

    return {
        "bonus_avios": bonus_avios,
        "spend_requirement_gbp": spend_requirement,
    }