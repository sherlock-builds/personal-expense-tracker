"""History page — browse, search, edit, and delete expenses."""

from datetime import date, datetime

import streamlit as st

from database import queries
from utils.constants import CATEGORIES, CATEGORY_OPTIONS, PAYMENT_METHODS, category_from_option
from utils.formatting import render_empty_state, render_expense_card
from utils.navigation import month_selector


def _parse_expense_date(value: str | date) -> date:
    if isinstance(value, date):
        return value
    return datetime.strptime(value[:10], "%Y-%m-%d").date()


@st.dialog("Edit Expense")
def edit_expense_dialog(expense: dict) -> None:
    expense_id = expense["id"]
    with st.form(f"edit_form_{expense_id}"):
        amount = st.number_input(
            "Amount (₹)",
            min_value=0.01,
            value=float(expense["amount"]),
            step=1.0,
            format="%.2f",
        )
        current_cat = expense["category"]
        cat_index = list(CATEGORIES.keys()).index(current_cat) if current_cat in CATEGORIES else 0
        category = st.selectbox("Category", CATEGORY_OPTIONS, index=cat_index)
        expense_date = st.date_input("Date", value=_parse_expense_date(expense["date"]))
        pm_index = (
            PAYMENT_METHODS.index(expense["payment_method"])
            if expense["payment_method"] in PAYMENT_METHODS
            else 0
        )
        payment_method = st.selectbox("Payment Method", PAYMENT_METHODS, index=pm_index)
        description = st.text_input("Description", value=expense.get("description") or "")

        col1, col2 = st.columns(2)
        with col1:
            save = st.form_submit_button("Save", type="primary", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("Cancel", use_container_width=True)

        if save:
            if amount <= 0:
                st.error("Amount must be greater than zero.")
            else:
                _, error = queries.update_expense(
                    expense_id=expense_id,
                    amount=amount,
                    category=category_from_option(category),
                    expense_date=expense_date,
                    payment_method=payment_method,
                    description=description,
                )
                if error:
                    st.error(error)
                else:
                    st.session_state.pop(f"confirm_delete_{expense_id}", None)
                    st.rerun()
        if cancel:
            st.rerun()


@st.dialog("Delete Expense")
def delete_expense_dialog(expense: dict) -> None:
    st.write(f"Are you sure you want to delete this expense?")
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
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Delete", type="primary", use_container_width=True):
            success, error = queries.delete_expense(expense["id"])
            if error:
                st.error(error)
            else:
                st.rerun()
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()


def render() -> None:
    st.markdown("## History")

    month, year = month_selector("history")

    search = st.text_input("Search by description", placeholder="Search...")
    col1, col2 = st.columns(2)
    with col1:
        category_filter = st.selectbox("Category", ["All"] + list(CATEGORIES.keys()))
    with col2:
        payment_filter = st.selectbox("Payment Method", ["All"] + PAYMENT_METHODS)

    expenses, error = queries.get_expenses(
        month=month,
        year=year,
        category=category_filter,
        payment_method=payment_filter,
        search=search,
    )
    if error:
        st.error(error)
        return

    if not expenses:
        st.markdown(
            render_empty_state("No expenses found.", "Try changing filters or add a new expense."),
            unsafe_allow_html=True,
        )
        return

    for expense in expenses:
        with st.container(border=True):
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
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Edit", key=f"edit_{expense['id']}", use_container_width=True):
                    edit_expense_dialog(expense)
            with col2:
                if st.button("Delete", key=f"delete_{expense['id']}", use_container_width=True):
                    delete_expense_dialog(expense)


render()
