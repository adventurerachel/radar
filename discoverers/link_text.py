"""
discoverers/link_text.py

Utilities for discovering URLs from webpage link text.

This module provides functionality to locate a hyperlink on a webpage
based on the text displayed to users, rather than requiring a known URL.

Example use case:
    A source website may publish a new article link each month while
    keeping the navigation text consistent. This module can find the
    current URL by searching for that text.
"""

import requests
from bs4 import BeautifulSoup


def discover_url_by_link_text(
    page_url: str,
    search_text: str
) -> str:
    """
    Find a URL from a webpage by matching hyperlink text.

    The function downloads a webpage, searches all anchor elements,
    and returns the URL of the first link whose visible text contains
    the supplied search text.

    Args:
        page_url:
            URL of the webpage containing the link to discover.

        search_text:
            Text expected to appear within the hyperlink.

    Returns:
        The URL contained in the matching anchor element.

    Raises:
        requests.HTTPError:
            If the webpage request fails.

        ValueError:
            If no matching hyperlink is found.

    Example:
        >>> discover_url_by_link_text(
        ...     "https://example.com",
        ...     "Barclaycard Avios Plus"
        ... )
        "https://example.com/article"
    """

    response = requests.get(
        page_url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    link = soup.find(
        "a",
        string=lambda s:
            s and search_text in s
    )

    if not link:
        raise ValueError(
            f"Could not find link text: {search_text}"
        )

    return link["href"]