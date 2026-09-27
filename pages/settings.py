"""Settings / More page."""

from datetime import date
from io import StringIO

import pandas as pd
import streamlit as st

from database import queries
from utils.constants import (
    APP_NAME,
    APP_VERSION,
    CATEGORIES,
    CURRENCY_CODE,
    CURRENCY_SYMBOL,
    PAYMENT_METHODS,
    category_display,
)
from utils.formatting import format_month_year
from utils.navigation import month_selector


def render() -> None:
    st.markdown("## More")

    st.markdown('<div class="section-header">Categories</div>', unsafe_allow_html=True)
    for name in CATEGORIES:
        st.markdown(
            f'<div class="settings-list-item">{category_display(name)}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-header">Payment Methods</div>', unsafe_allow_html=True)
    for method in PAYMENT_METHODS:
        st.markdown(
            f'<div class="settings-list-item">{method}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-header">Monthly Budget</div>', unsafe_allow_html=True)
    month, year = month_selector("settings")
    st.caption(format_month_year(month, year))

    current_budget, budget_error = queries.get_budget(month, year)
    if budget_error:
        st.error(budget_error)

    with st.form("budget_form"):
        budget_input = st.number_input(
            "Budget amount (₹)",
            min_value=0.0,
            value=float(current_budget) if current_budget else 0.0,
            step=500.0,
            format="%.0f",
        )
        if st.form_submit_button("Save Budget", type="primary", use_container_width=True):
            if budget_input <= 0:
                st.error("Budget must be greater than zero.")
            else:
                success, error = queries.set_budget(month, year, budget_input)
                if error:
                    st.error(error)
                else:
                    st.success(f"Budget set to {CURRENCY_SYMBOL}{budget_input:,.0f}")
                    st.rerun()

    st.markdown('<div class="section-header">Currency</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="settings-list-item">{CURRENCY_CODE} ({CURRENCY_SYMBOL})</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-header">Export Data</div>', unsafe_allow_html=True)
    expenses, export_error = queries.get_all_expenses()
    if export_error:
        st.error(export_error)
    elif expenses:
        df = pd.DataFrame(expenses)
        columns = [
            "date",
            "amount",
            "category",
            "payment_method",
            "description",
            "created_at",
        ]
        df = df[[c for c in columns if c in df.columns]]
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download CSV",
            data=csv_buffer.getvalue(),
            file_name=f"expenses_{date.today().isoformat()}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.caption("No expenses to export yet.")

    st.markdown('<div class="section-header">About</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="settings-list-item"><strong>{APP_NAME}</strong></div>
        <div class="settings-list-item">Version {APP_VERSION}</div>
        <div class="settings-list-item">Your personal finance companion.</div>
        """,
        unsafe_allow_html=True,
    )


render()
