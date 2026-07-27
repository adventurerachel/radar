"""
Mortgage tracker configuration.

Defines mortgage products and scenarios monitored by the
weekly mortgage tracker.
"""

MORTGAGE_MONITORS = [

    {
        "id": "mortgage_5yr_fixed",

        "name": (
            "5 Year Fixed Remortgage"
        ),

        "term_years": 5,

        "purpose": "remortgage",

        "sources": [
            "moneysupermarket",
            "accord",
        ],

        "scenarios": {
            "65_ltv": {
                "ltv": 65,
                "balance": 338000,
            },

            "70_ltv": {
                "ltv": 70,
                "balance": 350000,
            },
        },

        "remaining_term_years": 20,
    }

]