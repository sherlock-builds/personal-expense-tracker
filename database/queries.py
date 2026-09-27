"""Database query functions for expenses and budgets."""

from datetime import date, datetime
from typing import Any

from database.connection import DatabaseError, get_supabase_client


def _handle_response(response: Any, action: str) -> list[dict]:
    """Extract data from Supabase response or raise DatabaseError."""
    if hasattr(response, "data"):
        return response.data or []
    raise DatabaseError(f"Failed to {action}.")


def get_expenses(
    month: int | None = None,
    year: int | None = None,
    category: str | None = None,
    payment_method: str | None = None,
    search: str | None = None,
) -> tuple[list[dict], str | None]:
    """Fetch expenses with optional filters."""
    try:
        client = get_supabase_client()
        query = client.table("expenses").select("*")

        if month and year:
            start = date(year, month, 1).isoformat()
            if month == 12:
                end = date(year + 1, 1, 1).isoformat()
            else:
                end = date(year, month + 1, 1).isoformat()
            query = query.gte("date", start).lt("date", end)

        if category and category != "All":
            query = query.eq("category", category)

        if payment_method and payment_method != "All":
            query = query.eq("payment_method", payment_method)

        if search and search.strip():
            query = query.ilike("description", f"%{search.strip()}%")

        response = query.order("date", desc=True).order("created_at", desc=True).execute()
        return _handle_response(response, "fetch expenses"), None
    except DatabaseError as exc:
        return [], str(exc)
    except Exception:
        return [], "Unable to load expenses. Please try again."


def get_expense_by_id(expense_id: str) -> tuple[dict | None, str | None]:
    """Fetch a single expense by ID."""
    try:
        client = get_supabase_client()
        response = (
            client.table("expenses")
            .select("*")
            .eq("id", expense_id)
            .limit(1)
            .execute()
        )
        data = _handle_response(response, "fetch expense")
        return (data[0] if data else None), None
    except DatabaseError as exc:
        return None, str(exc)
    except Exception:
        return None, "Unable to load expense. Please try again."


def add_expense(
    amount: float,
    category: str,
    expense_date: date,
    payment_method: str,
    description: str | None = None,
) -> tuple[dict | None, str | None]:
    """Insert a new expense."""
    try:
        client = get_supabase_client()
        payload = {
            "amount": amount,
            "category": category,
            "date": expense_date.isoformat(),
            "payment_method": payment_method,
            "description": description.strip() if description else None,
        }
        response = client.table("expenses").insert(payload).execute()
        data = _handle_response(response, "add expense")
        return (data[0] if data else None), None
    except DatabaseError as exc:
        return None, str(exc)
    except Exception:
        return None, "Unable to save expense. Please try again."


def update_expense(
    expense_id: str,
    amount: float,
    category: str,
    expense_date: date,
    payment_method: str,
    description: str | None = None,
) -> tuple[dict | None, str | None]:
    """Update an existing expense."""
    try:
        client = get_supabase_client()
        payload = {
            "amount": amount,
            "category": category,
            "date": expense_date.isoformat(),
            "payment_method": payment_method,
            "description": description.strip() if description else None,
            "updated_at": datetime.utcnow().isoformat(),
        }
        response = (
            client.table("expenses").update(payload).eq("id", expense_id).execute()
        )
        data = _handle_response(response, "update expense")
        return (data[0] if data else None), None
    except DatabaseError as exc:
        return None, str(exc)
    except Exception:
        return None, "Unable to update expense. Please try again."


def delete_expense(expense_id: str) -> tuple[bool, str | None]:
    """Delete an expense by ID."""
    try:
        client = get_supabase_client()
        client.table("expenses").delete().eq("id", expense_id).execute()
        return True, None
    except DatabaseError as exc:
        return False, str(exc)
    except Exception:
        return False, "Unable to delete expense. Please try again."


def get_budget(month: int, year: int) -> tuple[float | None, str | None]:
    """Get monthly budget amount."""
    try:
        client = get_supabase_client()
        response = (
            client.table("monthly_budgets")
            .select("budget_amount")
            .eq("month", month)
            .eq("year", year)
            .limit(1)
            .execute()
        )
        data = _handle_response(response, "fetch budget")
        if not data:
            return None, None
        return float(data[0]["budget_amount"]), None
    except DatabaseError as exc:
        return None, str(exc)
    except Exception:
        return None, "Unable to load budget. Please try again."


def set_budget(month: int, year: int, amount: float) -> tuple[bool, str | None]:
    """Create or update monthly budget."""
    try:
        client = get_supabase_client()
        existing = (
            client.table("monthly_budgets")
            .select("id")
            .eq("month", month)
            .eq("year", year)
            .limit(1)
            .execute()
        )
        rows = _handle_response(existing, "check budget")

        payload = {
            "month": month,
            "year": year,
            "budget_amount": amount,
            "updated_at": datetime.utcnow().isoformat(),
        }

        if rows:
            client.table("monthly_budgets").update(payload).eq("id", rows[0]["id"]).execute()
        else:
            client.table("monthly_budgets").insert(payload).execute()

        return True, None
    except DatabaseError as exc:
        return False, str(exc)
    except Exception:
        return False, "Unable to save budget. Please try again."


def get_all_expenses() -> tuple[list[dict], str | None]:
    """Fetch all expenses for CSV export."""
    try:
        client = get_supabase_client()
        response = (
            client.table("expenses")
            .select("*")
            .order("date", desc=True)
            .order("created_at", desc=True)
            .execute()
        )
        return _handle_response(response, "export expenses"), None
    except DatabaseError as exc:
        return [], str(exc)
    except Exception:
        return [], "Unable to export data. Please try again."
