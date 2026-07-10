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


def monitor_article(url, extractor_names):

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

        extractor = EXTRACTOR_MAP[extractor_name]

        result[extractor_name] = extractor(soup)

    return result