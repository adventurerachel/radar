"""
Run the radar monitoring workflow.

This module coordinates the end-to-end radar process:

    1. Discover the current article URL
    2. Extract monitored information from the article
    3. Record the observation in history
    4. Compare against the previous snapshot
    5. Send an alert if a change is detected or otherwise specified

Individual responsibilities are delegated to separate modules:

    discoverers:
        Locate current article URLs

    monitors:
        Fetch pages and run extractors

    trackers:
        Store history and detect changes

    alerts:
        Format and send notifications

    Each monitor is processed independently. The latest extracted
    data is always stored in history. Notifications are sent when
    extracted data differs from the previous snapshot, or when an
    active special offer is detected.
"""

import logging

from config import MONITORS
from discoverers.link_text import discover_url_by_link_text
from trackers.history import append_history
from trackers.change_detector import has_changed
from alerts.pushover import send_alert
from monitors.page_monitor import monitor_article
from alerts.formatter import (
    format_alert_message,
    format_special_offer_alert,
)

logger = logging.getLogger(__name__)


def main() -> None:
    """
    Execute radar checks for all configured monitors.

    Each monitor is processed independently. The latest extracted
    data is always stored in history, while notifications are only
    sent when the extracted data differs from the previous snapshot.

    If an individual monitor fails, the error is logged and the
    remaining monitors continue processing.
    """

    for monitor in MONITORS:

        try:
            article_url = discover_url_by_link_text(
                monitor["category_url"],
                monitor["search_text"]
            )

            result = monitor_article(
                article_url,
                monitor["extractors"]
            )

            append_history(
                monitor["id"],
                result
            )

            changed = has_changed(
                monitor["id"],
                result
            )

            special_offer_active = result.get("special_offer") is not None

            if changed or special_offer_active:

                logger.info(
                    "%s: special offer detected",
                    monitor["name"]
                )

                message = format_special_offer_alert(
                    monitor["name"],
                    result
                )

                logger.info(message)

                send_alert(
                    monitor["name"],
                    message
                )

            else:
                logger.info(
                    "%s: no change",
                    monitor["name"]
                )

            logger.debug(result)

        except Exception:
            logger.exception(
                "%s: radar check failed",
                monitor["name"]
            )


if __name__ == "__main__":
    main()