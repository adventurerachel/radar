"""
Run the daily price tracking workflow.

Current purpose:
    - Load configured price monitors
    - Record price observations
    - Build historical price records

Retailer scraping will be added once the
tracking pipeline is proven.
"""

import logging

from price_config import PRICE_MONITORS
from trackers.history import append_history

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)


def collect_test_price(retailer: str) -> dict:
    """
    Temporary placeholder price collector.

    This will later be replaced with retailer-specific
    collectors.

    Args:
        retailer:
            Retailer identifier.

    Returns:
        Price observation.
    """

    return {
        "retailer": retailer,
        "price": 10.00,
        "regular_price": 13.00,
        "product_url": "https://example.com",
        "promotion_text": "Save £3",
    }


def main() -> None:
    """
    Execute price tracking workflow.
    """

    for monitor in PRICE_MONITORS:

        logger.info(
            "Checking %s",
            monitor["name"]
        )

        for retailer in monitor["retailers"]:

            observation = collect_test_price(retailer)

            append_history(
                monitor["id"],
                observation
            )

            logger.info(
                "%s: £%.2f",
                retailer,
                observation["price"]
            )


if __name__ == "__main__":
    main()