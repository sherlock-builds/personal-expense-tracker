"""Application constants for categories, payment methods, and budget states."""

APP_NAME = "Personal Expense Tracker"
APP_VERSION = "1.0"
CURRENCY_SYMBOL = "₹"
CURRENCY_CODE = "INR"

CATEGORIES = {
    "Food": "🍔",
    "Transport": "🚗",
    "Shopping": "🛍️",
    "Bills": "📄",
    "Entertainment": "🎬",
    "Health": "💊",
    "Travel": "✈️",
    "Education": "📚",
    "Work": "💼",
    "Other": "📌",
}

PAYMENT_METHODS = [
    "UPI",
    "Cash",
    "Credit Card",
    "Debit Card",
    "Bank Transfer",
    "Other",
]

CATEGORY_OPTIONS = [f"{icon} {name}" for name, icon in CATEGORIES.items()]

BUDGET_COMFORTABLE_MAX = 70
BUDGET_NEAR_MAX = 100

BUDGET_STATES = {
    "comfortable": {"label": "On track", "color": "#22C55E"},
    "near": {"label": "Near budget", "color": "#F59E0B"},
    "over": {"label": "Over budget", "color": "#EF4444"},
}

MONTH_NAMES = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def category_from_option(option: str) -> str:
    """Extract category name from selectbox option like '🍔 Food'."""
    parts = option.split(" ", 1)
    return parts[1] if len(parts) > 1 else option


def category_icon(category: str) -> str:
    """Return icon for a category name."""
    return CATEGORIES.get(category, "📌")


def category_display(category: str) -> str:
    """Return category with icon for display."""
    return f"{category_icon(category)} {category}"


def budget_state(percent_used: float) -> str:
    """Return budget state key based on percentage used."""
    if percent_used <= BUDGET_COMFORTABLE_MAX:
        return "comfortable"
    if percent_used <= BUDGET_NEAR_MAX:
        return "near"
    return "over"
