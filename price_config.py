"""
Price tracker configuration.

Defines products and retailers monitored by the daily price tracker.

Each price monitor provides:
    - Product identity
    - Retailers to check
    - Alert thresholds
"""


PRICE_MONITORS = [

    {
        "id": "scrumbles_turkey_2kg",

        "name": (
            "Scrumbles Turkey Adult & Senior "
            "Dry Dog Food 2kg"
        ),

        # Alert when the product reaches this price
        # or below.
        "target_price": 10.00,

        "retailers": [
            "waitrose",
            "tesco",
            "sainsburys",
            "asda",
            "pets_at_home",
        ],
    }

]