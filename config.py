"""
Radar monitor configuration.

This module defines the websites and data points that the radar
should monitor.

Each monitor configuration provides the information required by the
radar workflow:

    - Where to find the current article URL
    - How to identify the article
    - Which extractors to run
    - How the monitor is identified for snapshots and history

Adding a new monitor should only require adding a new configuration
entry here. The monitoring workflow remains unchanged.
"""


MONITORS = [

    {
        "name": "Barclaycard Avios Plus",

        # Unique identifier used for snapshots and history storage.
        "id": "barclaycard",

        # Page containing links to the latest article.
        "category_url": "https://www.headforpoints.com/category/barclaycard-avios-mastercard/",

        # Text used to locate the current article link.
        "search_text":
            "review of the paid-for Barclaycard Avios Plus Mastercard is here",

        # Extractors to run against the article page.
        "extractors": [
            "special_offer",
            "update_date",
            "barclaycard_bonus"
        ]
    },

    {
        "name": "HSBC Premier",

        # Unique identifier used for snapshots and history storage.
        "id": "hsbc",

        "category_url": "https://www.headforpoints.com/category/hsbc-premier-mastercard/",

        "search_text":
            "our review of the free HSBC Premier Credit Card here",

        "extractors": [
            "special_offer",
            "update_date",
            "hsbc_conclusion"
        ]
    }
]