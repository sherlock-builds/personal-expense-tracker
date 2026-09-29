"""Home page — current month overview."""

import streamlit as st

from database import queries
from utils.calculations import recent_expenses, spending_by_category, total_spending
from utils.components import render_budget_progress
from utils.formatting import (
    format_currency,
    render_category_row,
    render_empty_state,
    render_expense_card,
)
from utils.navigation import month_selector


def render() -> None:
    month, year = month_selector("home")

    expenses, error = queries.get_expenses(month=month, year=year)
    if error:
        st.error(error)
        return

    budget, budget_error = queries.get_budget(month, year)
    if budget_error:
        st.error(budget_error)
        return

    total = total_spending(expenses)

    st.markdown(
        f"""
        <div class="summary-card">
            <div class="total-spend">{format_currency(total)}</div>
            <div class="total-spend-label">spent this month</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_budget_progress(total, budget)

    st.markdown('<div class="section-header">By Category</div>', unsafe_allow_html=True)
    by_category = spending_by_category(expenses)
    if by_category:
        max_amount = max(by_category.values())
        for category, amount in by_category.items():
            st.markdown(render_category_row(category, amount, max_amount), unsafe_allow_html=True)
    else:
        st.markdown(
            render_empty_state("No category spending yet.", "Add an expense to see breakdown."),
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-header">Recent Expenses</div>', unsafe_allow_html=True)
    recent = recent_expenses(expenses, limit=5)
    if recent:
        for expense in recent:
            st.markdown(
                render_expense_card(
                    expense["category"],
                    expense.get("description"),
                    expense["date"],
                    expense["payment_method"],
                    float(expense["amount"]),
                ),
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            render_empty_state("No expenses this month.", "Tap Add to record your first expense."),
            unsafe_allow_html=True,
        )

    # In-page brand row (visible inside pages so it's present in the client DOM)
    st.markdown(
        '<div class="inpage-brand-row">Developed by — Sherlock • Expense Tracker</div>',
        unsafe_allow_html=True,
    )


render()
