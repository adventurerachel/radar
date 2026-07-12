"""
Extract highlighted "Special Offer" content from an article.

The offer is identified by a specific CSS class and text prefix used
by the source website to visually emphasise promotional content.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bs4 import BeautifulSoup

def extract_special_offer(soup) -> str | None:
    """
    Extract the article's highlighted special-offer text.

    The function searches all paragraph elements and returns the first
    paragraph that:

    - Uses the site's special-offer text colour
    - Begins with "SPECIAL OFFER"

    Args:
        soup:
            Parsed article HTML as a BeautifulSoup object.

    Returns:
        The special-offer text if found, otherwise None.
    """

    for p in soup.find_all("p"):

        classes = p.get("class", [])
        text = p.get_text(" ", strip=True)

        # The source site highlights promotional offers using the
        # "has-vivid-red-color" CSS class.
        if (
            "has-vivid-red-color" in classes
            and text.upper().startswith("SPECIAL OFFER")
        ):
            return text

    return None