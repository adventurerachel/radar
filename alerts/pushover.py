import os
import requests

from dotenv import load_dotenv

load_dotenv()

PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")


def send_alert(title, message):

    print("Sending Pushover alert...")
    print(f"Title: {title}")

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

    print("Pushover response:")
    print(response.status_code)
    print(response.text)

    # response = requests.post(
    #     "https://api.pushover.net/1/messages.json",
    #     data={
    #         "token": PUSHOVER_API_TOKEN,
    #         "user": PUSHOVER_USER_KEY,
    #         "title": title,
    #         "message": message,
    #     },
    #     timeout=30
    # )

    # print(f"Pushover response: {response.status_code} {response.text}")

    response.raise_for_status()