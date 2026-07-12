"""
Extract the conclusion summary from an HSBC article.

The conclusion section is used as a concise representation of the
article's current recommendation or assessment. Monitoring this
section helps detect meaningful editorial changes without comparing
the entire article body.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bs4 import BeautifulSoup

def extract_hsbc_conclusion(soup) -> str | None:
    """
    Extract the first paragraph under the article's "Conclusion" heading.

    The function searches for an <h2> element whose text is exactly
    "Conclusion" (case-insensitive), then returns the first paragraph
    that follows it.

    Args:
        soup:
            Parsed article HTML as a BeautifulSoup object.

    Returns:
        The conclusion text if found, otherwise None.
    """

    heading = soup.find(
        "h2",
        string=lambda x:
            x and x.strip().lower() == "conclusion"
    )

    if not heading:
        return None

    # Retrieve the first paragraph following the Conclusion heading.
    paragraph = heading.find_next("p")

    if not paragraph:
        return None

    return paragraph.get_text(
        " ",
        strip=True
    )