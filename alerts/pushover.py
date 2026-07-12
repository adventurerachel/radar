"""
Send radar notifications through Pushover.

This module handles communication with the Pushover API.
Authentication credentials are loaded from environment variables
to avoid storing secrets in source code.

The module validates that required credentials are available when
loaded and raises an error immediately if configuration is missing.

Required environment variables:
    PUSHOVER_USER_KEY:
        Target Pushover user identifier.

    PUSHOVER_API_TOKEN:
        Application API token used to authenticate requests.

Raises:
    RuntimeError:
        If required Pushover credentials are not configured.
"""

import os
import logging
import requests

from dotenv import load_dotenv


load_dotenv()

PUSHOVER_USER_KEY = os.environ.get("PUSHOVER_USER_KEY")
PUSHOVER_API_TOKEN = os.environ.get("PUSHOVER_API_TOKEN")

if not PUSHOVER_USER_KEY or not PUSHOVER_API_TOKEN:
    raise RuntimeError(
        "Missing Pushover credentials. "
        "Set PUSHOVER_USER_KEY and PUSHOVER_API_TOKEN."
    )

logger = logging.getLogger(__name__)


def send_alert(title: str, message: str) -> None:
    """
    Send a notification through Pushover.

    Args:
        title:
            Notification title displayed to the user.

        message:
            Notification body text.

    Raises:
        requests.HTTPError:
            If the Pushover API request fails.

    Notes:
        Pushover credentials are validated when this module is imported.

    Example:
        send_alert(
            "Barclaycard update",
            "Bonus increased to 50,000 Avios"
        )
    """

    logger.info("Sending Pushover alert: %s", title)

    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": PUSHOVER_API_TOKEN,
            "user": PUSHOVER_USER_KEY,
            "title": title,
            "message": message,
        },
        timeout=30
    )

    logger.info(
        "Pushover response: %s %s",
        response.status_code,
        response.text
    )

    response.raise_for_status()