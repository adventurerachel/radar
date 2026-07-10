from bs4 import BeautifulSoup

from extractors.special_offer import extract_special_offer

html = "<p>No special offer here</p>"

soup = BeautifulSoup(html, "html.parser")

print(extract_special_offer(soup))