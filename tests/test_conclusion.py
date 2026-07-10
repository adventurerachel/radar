from bs4 import BeautifulSoup

from extractors.conclusion import extract_conclusion

from bs4 import BeautifulSoup

from extractors.conclusion import extract_conclusion

from monitors.page_monitor import monitor_page

result = monitor_page(
    "https://www.headforpoints.com/2026/06/19/review-hsbc-premier-credit-card/"
)

print(result)