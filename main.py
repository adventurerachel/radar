from config import MONITORS
from discoverers.link_text import discover_url_by_link_text
from trackers.history import append_history
from trackers.change_detector import has_changed
from alerts.pushover import send_alert
from monitors.page_monitor import monitor_article
from alerts.formatter import format_alert_message


def main():

    for monitor in MONITORS:

        article_url = discover_url_by_link_text(
            monitor["category_url"],
            monitor["search_text"]
        )

        result = monitor_article(
            article_url,
            monitor["extractors"]
        )

        changed = has_changed(
            monitor["history_file"],
            result
        )

        append_history(
            monitor["history_file"],
            result
        )

        if changed:

            print("CHANGE DETECTED")

            message = format_alert_message(
                monitor["name"],
                result
            )

            print(message)

            send_alert(
                monitor["name"],
                message
            )

        else:
            print("No change detected")

        print(result)

if __name__ == "__main__":
    main()