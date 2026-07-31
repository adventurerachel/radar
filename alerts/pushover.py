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

import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(
    Path(__file__).resolve().parents[1] / ".env"
)

PUSHOVER_USER_KEY = os.environ["PUSHOVER_USER_KEY"]
PUSHOVER_API_TOKEN = os.environ["PUSHOVER_API_TOKEN"]
PUSHOVER_URL="https://api.pushover.net/1/messages.json"

if not PUSHOVER_USER_KEY or not PUSHOVER_API_TOKEN:
    raise RuntimeError(
        "Missing Pushover credentials. "
        "Set PUSHOVER_USER_KEY and PUSHOVER_API_TOKEN."
    )

logger = logging.getLogger(__name__)


def send_pushover(
    title: str,
    message: str,
    priority: int = 0,
) -> None:
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
        send_pushover(
            "Barclaycard update",
            "Bonus increased to 50,000 Avios"
        )
    """

    logger.info("Sending Pushover alert: %s", title)

    response = requests.post(
        PUSHOVER_URL,
        data={
            "token": PUSHOVER_API_TOKEN,
            "user": PUSHOVER_USER_KEY,
            "title": title,
            "message": message,
            "priority": priority,
        },
        timeout=30
    )

    logger.info(
        "Pushover response: %s %s",
        response.status_code,
        response.text
    )

    response.raise_for_status()

def send_alert(
    title: str,
    message: str,
) -> None:
    """
    Backwards-compatible wrapper.
    """

    send_pushover(
        title,
        message,
    )