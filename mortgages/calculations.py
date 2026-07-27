"""
Mortgage calculation helpers.
"""

def calculate_monthly_payment(
    balance: float,
    annual_rate: float,
    years: int,
) -> float:
    """
    Calculate monthly repayment for a repayment mortgage.
    """

    monthly_rate = annual_rate / 100 / 12
    payments = years * 12

    payment = (
        balance
        * monthly_rate
        * (1 + monthly_rate) ** payments
        /
        ((1 + monthly_rate) ** payments - 1)
    )

    return round(payment, 2)

def calculate_interest_paid(
    balance: float,
    annual_rate: float,
    years_remaining: int,
    fixed_period_years: int = 5,
) -> float:
    """
    Calculate interest paid during the fixed mortgage period.

    Assumes a repayment mortgage with monthly payments.

    Args:
        balance:
            Starting mortgage balance.

        annual_rate:
            Annual mortgage interest rate as a percentage.

        years_remaining:
            Remaining mortgage term.

        fixed_period_years:
            Length of fixed period being analysed.

    Returns:
        Total interest paid during fixed period.
    """

    monthly_payment = calculate_monthly_payment(
        balance,
        annual_rate,
        years_remaining,
    )

    monthly_rate = annual_rate / 100 / 12

    balance_remaining = balance
    total_interest = 0

    months = fixed_period_years * 12

    for _ in range(months):

        interest = (
            balance_remaining
            * monthly_rate
        )

        principal = (
            monthly_payment
            - interest
        )

        total_interest += interest

        balance_remaining -= principal

    return round(total_interest, 2)