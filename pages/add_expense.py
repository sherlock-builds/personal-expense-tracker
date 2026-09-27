"""Add Expense page — quick expense entry."""

from datetime import date

import streamlit as st

from database import queries
from utils.constants import CATEGORY_OPTIONS, PAYMENT_METHODS, category_from_option


def _clear_form() -> None:
    st.session_state.add_amount = 0.0
    st.session_state.add_category = CATEGORY_OPTIONS[0]
    st.session_state.add_date = date.today()
    st.session_state.add_payment = PAYMENT_METHODS[0]
    st.session_state.add_description = ""


def render() -> None:
    st.markdown("## Add Expense")
    st.caption("Record a new expense in seconds.")

    if "add_amount" not in st.session_state:
        _clear_form()

    if st.session_state.get("expense_added"):
        st.success("Expense added successfully!")
        st.session_state.expense_added = False

    with st.form("add_expense_form", clear_on_submit=False):
        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=1.0,
            format="%.2f",
            key="add_amount",
        )
        category = st.selectbox("Category", CATEGORY_OPTIONS, key="add_category")
        expense_date = st.date_input("Date", key="add_date")
        payment_method = st.selectbox("Payment Method", PAYMENT_METHODS, key="add_payment")
        description = st.text_input("Description (optional)", key="add_description")

        submitted = st.form_submit_button("Add Expense", type="primary", use_container_width=True)

        if submitted:
            if amount <= 0:
                st.error("Amount must be greater than zero.")
            elif not category:
                st.error("Please select a category.")
            else:
                category_name = category_from_option(category)
                result, error = queries.add_expense(
                    amount=amount,
                    category=category_name,
                    expense_date=expense_date,
                    payment_method=payment_method,
                    description=description,
                )
                if error:
                    st.error(error)
                else:
                    st.session_state.expense_added = True
                    _clear_form()
                    st.rerun()


render()
