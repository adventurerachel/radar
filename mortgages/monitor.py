"""
Run weekly mortgage tracking workflow.
"""

from mortgage_config import MORTGAGE_MONITORS
from trackers.history import append_history
from mortgages.calculations import (
    calculate_monthly_payment,
    calculate_interest_paid,
)


def collect_test_rate(
    scenario: str,
    config: dict,
) -> dict:
    """
    Temporary mortgage observation.

    Replace with real source collectors later.
    """

    rate = 4.00
    product_fee = 999

    interest_cost = calculate_interest_paid(
        config["balance"],
        rate,
        config["remaining_term_years"],
    )

    monthly_payment = calculate_monthly_payment(
        config["balance"],
        rate,
        config["remaining_term_years"],
    )

    return {
        "source": "test",
        "source_url": "https://example.com",

        "scenario": scenario,

        "provider": "Example Bank",
        "product_name": "5 Year Fixed Remortgage",

        "term_years": config["term_years"],
        "ltv": config["ltv"],
        "balance": config["balance"],

        "rate": rate,
        "product_fee": 999,

        "monthly_payment": monthly_payment,

        "interest_cost_5yr": interest_cost,

        "total_cost_5yr": (
            interest_cost
            + product_fee
        ),
    }

def main():

    for monitor in MORTGAGE_MONITORS:

        for scenario, details in monitor["scenarios"].items():

            observation = collect_test_rate(
                scenario,
                {
                    **monitor,
                    **details,
                },
            )

            append_history(
                monitor["id"],
                observation,
            )


if __name__ == "__main__":
    main()