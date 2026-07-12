"""
Monitor webpages and extract configured article data.

This module handles the common workflow for monitored articles:

    URL
     |
     v
 Fetch HTML
     |
     v
 Parse with BeautifulSoup
     |
     v
 Run configured extractors
     |
     v
 Return structured results

Individual extraction logic is kept separate in the extractors
package. This module only coordinates fetching and extraction.
"""

import requests
from bs4 import BeautifulSoup

from extractors.update_date import extract_update_date
from extractors.special_offer import extract_special_offer
from extractors.barclaycard import extract_barclaycard_bonus
from extractors.hsbc import extract_hsbc_conclusion


EXTRACTOR_MAP = {
    "update_date": extract_update_date,
    "special_offer": extract_special_offer,
    "barclaycard_bonus": extract_barclaycard_bonus,
    "hsbc_conclusion": extract_hsbc_conclusion,
}


def monitor_article(
    url: str,
    extractor_names: list[str],
) -> dict:
    """
    Fetch an article and extract configured information.

    Args:
        url:
            Article URL to monitor.

        extractor_names:
            List of extractor names to run. Names must exist in
            EXTRACTOR_MAP.

    Returns:
        Dictionary containing:
            - source_url:
                URL of the monitored article.
            - Extracted fields returned by the selected extractors.

    Raises:
        requests.HTTPError:
            If the article cannot be retrieved.

        KeyError:
            If an unknown extractor name is supplied.

    Example:
        monitor_article(
            "https://example.com/article",
            ["update_date", "special_offer"]
        )

        Returns:
            {
                "source_url": "https://example.com/article",
                "update_date": "12 July 2026",
                "special_offer": "Earn 25,000 Avios"
            }
    """

    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    result = {
        "source_url": url
    }

    for extractor_name in extractor_names:

        extractor = EXTRACTOR_MAP.get(extractor_name)

        if not extractor:
            raise ValueError(
                f"Unknown extractor: {extractor_name}"
            )

        result[extractor_name] = extractor(soup)

    return result