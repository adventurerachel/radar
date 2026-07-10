import requests
from bs4 import BeautifulSoup


def discover_url_by_link_text(
    page_url,
    search_text
):
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