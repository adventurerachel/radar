import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

from .base import BaseMonitor

BASE = "https://www.headforpoints.com"
LIST_URL = "https://www.headforpoints.com/category/barclaycard-avios-mastercard/"


class BarclaycardMonitor(BaseMonitor):
    name = "barclaycard"

    def collect(self) -> dict:
        list_html = requests.get(LIST_URL, timeout=20).text
        soup = BeautifulSoup(list_html, "html.parser")

        # find latest article link
        link = soup.select_one("h2.entry-title a")
        if not link:
            return {"error": "no article found"}

        article_url = urljoin(BASE, link["href"])

        article_html = requests.get(article_url, timeout=20).text
        article_text = BeautifulSoup(article_html, "html.parser").get_text(" ", strip=True)

        return self._parse(article_text, article_url)

    def _parse(self, text: str, url: str) -> dict:
        text = text.lower()

        avios = re.search(r"(\d{10,})\s*avios", text)
        spend = re.search(r"£\s?(\d{2,5})", text)

        return {
        "card_name": "barclaycard avios plus",
        "bonus_avios": int(avios.group(1)) if avios else None,
        "spend_requirement_gbp": int(spend.group(1)) if spend else None,
        "source_url": url,
        }