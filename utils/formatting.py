"""Display formatting helpers."""

from datetime import date, datetime

from utils.constants import CURRENCY_SYMBOL, MONTH_NAMES, category_display, category_icon


def format_currency(amount: float | int | None) -> str:
    """Format amount as INR currency string."""
    if amount is None:
        return f"{CURRENCY_SYMBOL}0"
    return f"{CURRENCY_SYMBOL}{float(amount):,.0f}"


def format_month_year(month: int, year: int) -> str:
    """Format month and year as 'September 2026'."""
    return f"{MONTH_NAMES[month - 1]} {year}"


def format_date(value: date | str | None) -> str:
    """Format date for display."""
    if value is None:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        except ValueError:
            value = datetime.strptime(value[:10], "%Y-%m-%d").date()
    return value.strftime("%b %d")


def format_date_long(value: date | str | None) -> str:
    """Format date as 'September 18'."""
    if value is None:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        except ValueError:
            value = datetime.strptime(value[:10], "%Y-%m-%d").date()
    return f"{MONTH_NAMES[value.month - 1]} {value.day}"


def expense_title(description: str | None, category: str) -> str:
    """Return display title for an expense."""
    if description and description.strip():
        return description.strip()
    return category


def render_expense_card(
    category: str,
    description: str | None,
    expense_date: date | str,
    payment_method: str,
    amount: float,
) -> str:
    """Render HTML for a single expense feed card."""
    title = expense_title(description, category)
    icon = category_icon(category)
    return f"""
    <div class="expense-card">
        <div class="expense-card-left">
            <div class="expense-icon">{icon}</div>
            <div class="expense-details">
                <div class="expense-title">{title}</div>
                <div class="expense-meta">{category} · {payment_method} · {format_date(expense_date)}</div>
            </div>
        </div>
        <div class="expense-amount">{format_currency(amount)}</div>
    </div>
    """


def render_category_row(category: str, amount: float, max_amount: float) -> str:
    """Render HTML for a category summary row with mini bar."""
    icon = category_icon(category)
    bar_width = (amount / max_amount * 100) if max_amount > 0 else 0
    return f"""
    <div class="category-row">
        <div class="category-row-header">
            <span class="category-label">{icon} {category}</span>
            <span class="category-amount">{format_currency(amount)}</span>
        </div>
        <div class="category-bar-track">
            <div class="category-bar-fill" style="width: {bar_width}%;"></div>
        </div>
    </div>
    """


def render_stat_card(label: str, value: str, subtext: str = "") -> str:
    """Render a simple stat card."""
    sub = f'<div class="stat-subtext">{subtext}</div>' if subtext else ""
    return f"""
    <div class="stat-card">
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
        {sub}
    </div>
    """


def render_empty_state(message: str, hint: str = "") -> str:
    """Render an empty state message."""
    hint_html = f'<p class="empty-hint">{hint}</p>' if hint else ""
    return f"""
    <div class="empty-state">
        <p class="empty-message">{message}</p>
        {hint_html}
    </div>
    """
