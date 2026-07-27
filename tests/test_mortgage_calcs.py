"""
Tests for mortgage calculation helpers.
"""

from mortgages.calculations import (
    calculate_monthly_payment,
    calculate_interest_paid,
)


def test_calculate_monthly_payment():
    """
    Test repayment calculation for a known mortgage example.
    """

    payment = calculate_monthly_payment(
        balance=338000,
        annual_rate=4.0,
        years=20,
    )

    assert payment == 2048.21


def test_calculate_interest_paid():
    """
    Test interest calculation over the fixed period.
    """

    interest = calculate_interest_paid(
        balance=338000,
        annual_rate=4.0,
        years_remaining=20,
        fixed_period_years=5,
    )

    assert interest == 61795.22


def test_interest_paid_is_less_than_total_payments():
    """
    Sanity check that interest is only part of total repayments.
    """

    payment = calculate_monthly_payment(
        balance=338000,
        annual_rate=4.0,
        years=20,
    )

    interest = calculate_interest_paid(
        balance=338000,
        annual_rate=4.0,
        years_remaining=20,
        fixed_period_years=5,
    )

    five_year_payments = payment * 60

    assert interest < five_year_payments