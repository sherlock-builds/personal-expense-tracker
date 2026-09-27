"""Calculation helpers for expense analytics."""

from calendar import monthrange
from collections import defaultdict
from datetime import date, datetime

import pandas as pd


def _parse_date(value: date | str) -> date:
    if isinstance(value, date):
        return value
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        return datetime.strptime(value[:10], "%Y-%m-%d").date()


def total_spending(expenses: list[dict]) -> float:
    """Sum all expense amounts."""
    return sum(float(e["amount"]) for e in expenses)


def spending_by_category(expenses: list[dict]) -> dict[str, float]:
    """Group spending by category."""
    totals: dict[str, float] = defaultdict(float)
    for expense in expenses:
        totals[expense["category"]] += float(expense["amount"])
    return dict(sorted(totals.items(), key=lambda x: x[1], reverse=True))


def recent_expenses(expenses: list[dict], limit: int = 5) -> list[dict]:
    """Return most recent expenses."""
    sorted_expenses = sorted(
        expenses,
        key=lambda e: (_parse_date(e["date"]), e.get("created_at", "")),
        reverse=True,
    )
    return sorted_expenses[:limit]


def budget_stats(total_spent: float, budget: float | None) -> dict:
    """Calculate budget usage statistics."""
    if not budget or budget <= 0:
        return {
            "budget": None,
            "spent": total_spent,
            "remaining": None,
            "percent_used": None,
        }

    remaining = budget - total_spent
    percent_used = (total_spent / budget) * 100
    return {
        "budget": budget,
        "spent": total_spent,
        "remaining": remaining,
        "percent_used": percent_used,
    }


def average_daily_spending(expenses: list[dict], month: int, year: int) -> float:
    """Calculate average daily spending for a month."""
    total = total_spending(expenses)
    if total == 0:
        return 0.0

    today = date.today()
    if year == today.year and month == today.month:
        days = max(today.day, 1)
    else:
        days = monthrange(year, month)[1]

    return total / days


def largest_expense(expenses: list[dict]) -> dict | None:
    """Find the largest single expense."""
    if not expenses:
        return None
    return max(expenses, key=lambda e: float(e["amount"]))


def highest_spending_day(expenses: list[dict]) -> dict | None:
    """Find the day with highest total spending."""
    if not expenses:
        return None

    daily: dict[date, float] = defaultdict(float)
    for expense in expenses:
        d = _parse_date(expense["date"])
        daily[d] += float(expense["amount"])

    best_day = max(daily, key=lambda d: daily[d])
    return {"date": best_day, "amount": daily[best_day]}


def daily_spending_trend(expenses: list[dict]) -> pd.DataFrame:
    """Return daily spending totals as a DataFrame."""
    if not expenses:
        return pd.DataFrame(columns=["date", "amount"])

    daily: dict[date, float] = defaultdict(float)
    for expense in expenses:
        d = _parse_date(expense["date"])
        daily[d] += float(expense["amount"])

    rows = [{"date": d, "amount": daily[d]} for d in sorted(daily.keys())]
    return pd.DataFrame(rows)


def category_chart_data(expenses: list[dict]) -> pd.DataFrame:
    """Return category totals as a DataFrame for charts."""
    by_cat = spending_by_category(expenses)
    if not by_cat:
        return pd.DataFrame(columns=["category", "amount"])

    return pd.DataFrame(
        [{"category": k, "amount": v} for k, v in by_cat.items()]
    )


def month_comparison(
    current_total: float,
    previous_total: float,
    previous_month: int,
    previous_year: int,
) -> str | None:
    """Return comparison text vs previous month."""
    from utils.constants import MONTH_NAMES

    if previous_total == 0 and current_total == 0:
        return None

    diff = current_total - previous_total
    month_name = MONTH_NAMES[previous_month - 1]

    if diff == 0:
        return f"Same as {month_name}"
    if diff > 0:
        return f"₹{abs(diff):,.0f} more than {month_name}"
    return f"₹{abs(diff):,.0f} less than {month_name}"


def previous_month_year(month: int, year: int) -> tuple[int, int]:
    """Return previous month and year."""
    if month == 1:
        return 12, year - 1
    return month - 1, year
