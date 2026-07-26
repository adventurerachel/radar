"""
Daily Scrumbles price monitor.

Checks:
    Scrumbles Turkey Adult & Senior Dry Dog Food 2kg

Retailers:
    - Waitrose
    - Tesco
    - Sainsbury's
    - Asda
    - Pets at Home

Output:
    JSONL file:
        storage/dog_food_prices.jsonl

Each execution appends one record per retailer.

Schema captures:
    - standard price
    - promotional price
    - loyalty pricing
    - effective customer price
    - promotion details
    - source information
"""

from __future__ import annotations

import json
from datetime import datetime, UTC
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from project root
load_dotenv(
    Path(__file__).resolve().parents[1] / ".env"
)

client = OpenAI()


PRODUCT_ID = "scrumbles_turkey_2kg"
DATASET = "dog_food_prices"

OUTPUT_FILE = Path(
    "storage/dog_food_prices.jsonl"
)


EXPECTED_RETAILERS = {
    "waitrose",
    "tesco",
    "sainsburys",
    "asda",
    "petsathome",
}

EXPECTED_AVAILABILITY = {
    "in_stock",
    "out_of_stock",
    "unknown",
}


EXPECTED_SOURCE_TYPES = {
    "retailer_product_page",
    "retailer_category_page",
    "comparison_site",
    "other",
}

EXPECTED_PRICE_SOURCES = {
    "retailer",
    "third_party",
    "unknown",
}

today = datetime.now(
    UTC
).date().isoformat()


PROMPT = f"""
Today's date is {today}.

Find prices available on or after this date for:

Scrumbles Turkey Adult & Senior Dry Dog Food 2kg

Retailers:

- Waitrose
- Tesco
- Sainsbury's
- Asda
- Pets at Home

Return JSON only.

Schema:

Schema:

{{
  "prices": [
    {{
      "retailer": "tesco",
      "regular_price": 12.00,
      "promo_price": 9.00,
      "effective_price": 9.00,
      "promotion_active": true,
      "promo_type": "Clubcard",
      "promo_description": "Clubcard Price",
      "availability": "in_stock",
      "source_type": "retailer_product_page",
      "price_source": "retailer",
      "note": "Clubcard Price until 18 August 2026",
      "currency": "GBP",
      "found": true,
      "confidence": "high",
      "source_url": "https://...",
      "source_date": "{today}"
    }}
  ]
}}

Rules:

- Use null when unavailable.
- effective_price is the price a customer pays today.
- If no promotion exists:
    - regular_price = effective_price
    - promo_price = null
    - promotion_active = false
- Capture loyalty prices:
    Examples:
        Clubcard
        Nectar
        Rewards
- Include source_url where possible.
- price_source must be:
    retailer
    third_party
    unknown
- Use:
    retailer = price taken directly from retailer website
    third_party = price taken from comparison site or aggregator
    unknown = cannot determine
- Only mark found=true if the price can be confidently linked to the exact product.
- Do not use unrelated products or approximate matches.
- Third-party comparison sites may be used only when:
    - the exact product matches,
    - the retailer is clearly identified,
    - no retailer page is available.
- Include source_date where possible.
- Confidence:
    high = direct retailer page
    medium = comparison site
    low = search snippet/inference
- Retailer names must be lowercase:
    waitrose
    tesco
    sainsburys
    asda
    petsathome
- availability must be:
    in_stock
    out_of_stock
    unknown
- source_type must be:
    retailer_product_page
    retailer_category_page
    comparison_site
    other
- Prefer retailer product pages over comparison sites.
- Clearly state when a price is found but the product is unavailable.
"""


def utc_timestamp() -> str:
    """
    Return current UTC timestamp.
    """

    return datetime.now(
        UTC
    ).isoformat()


def fetch_prices() -> list[dict[str, Any]]:
    """
    Ask the model to retrieve current prices.

    Returns:
        List of retailer price records.
    """

    response = client.responses.create(
        model="gpt-5-mini",
        tools=[
            {
                "type": "web_search"
            }
        ],
        input=PROMPT,
    )

    data = json.loads(
        response.output_text
    )

    return data["prices"]


def existing_records() -> set[tuple[str, str, str]]:
    """
    Load existing JSONL keys.

    Prevents duplicate entries if
    GitHub Actions is manually rerun.

    Key:
        (date, product, retailer)
    """

    if not OUTPUT_FILE.exists():
        return set()

    keys = set()

    with OUTPUT_FILE.open(
        encoding="utf-8"
    ) as file:

        for line in file:
            try:
                row = json.loads(line)

                keys.add(
                    (
                        row["date"],
                        row["product"],
                        row["retailer"],
                    )
                )

            except (
                KeyError,
                json.JSONDecodeError,
            ):
                continue

    return keys


def save_prices(
    prices: list[dict[str, Any]]
) -> int:

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    date = datetime.now(
        UTC
    ).date().isoformat()

    timestamp = utc_timestamp()

    existing = existing_records()

    written = 0

    with OUTPUT_FILE.open(
        "a",
        encoding="utf-8",
    ) as file:

        for price in prices:

            retailer = price.get(
                "retailer"
            )

            if retailer not in EXPECTED_RETAILERS:
                continue

            key = (
                date,
                PRODUCT_ID,
                retailer,
            )

            if key in existing:
                continue


            availability = price.get(
                "availability",
                "unknown",
            )

            if availability not in EXPECTED_AVAILABILITY:
                availability = "unknown"


            source_type = price.get(
                "source_type",
                "unknown",
            )

            if source_type not in EXPECTED_SOURCE_TYPES:
                source_type = "unknown"


            effective_price = price.get(
                "effective_price"
            )
            price_source = price.get(
                "price_source",
                "unknown",
            )

            if price_source not in EXPECTED_PRICE_SOURCES:
                price_source = "unknown"

            record = {
                "timestamp": timestamp,
                "date": date,
                "dataset": DATASET,
                "product": PRODUCT_ID,
                "retailer": retailer,

                "price": effective_price,
                "regular_price": price.get(
                    "regular_price"
                ),
                "promo_price": price.get(
                    "promo_price"
                ),
                "effective_price": effective_price,

                "promotion_active": price.get(
                    "promotion_active",
                    False,
                ),

                "promo_type": price.get(
                    "promo_type"
                ),

                "promo_description": price.get(
                    "promo_description"
                ),

                "note": price.get(
                    "note"
                ),

                "currency": price.get(
                    "currency",
                    "GBP",
                ),

                "found": price.get(
                    "found",
                    False,
                ),

                "confidence": price.get(
                    "confidence"
                ),

                "availability": availability,

                "source_type": source_type,

                "price_source": price_source,

                "source_url": price.get(
                    "source_url"
                ),

                "source_date": price.get(
                    "source_date"
                ),
            }


            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )

            written += 1

    return written


def main() -> None:
    """
    Run daily monitor.
    """

    start_time = datetime.now(
        UTC
    )

    prices = fetch_prices()

    saved = save_prices(
        prices
    )

    end_time = datetime.now(
        UTC
    )

    runtime = end_time - start_time

    seconds = runtime.total_seconds()

    if seconds < 60:
        runtime_display = (
            f"{seconds:.1f} seconds"
        )
    else:
        minutes = int(seconds // 60)
        remaining = int(seconds % 60)
        runtime_display = (
            f"{minutes}m {remaining}s"
        )

    print(
        f"Saved {saved} records"
    )

    print(
        f"Runtime: {runtime_display}"
    )


if __name__ == "__main__":
    main()