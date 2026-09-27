"""Reusable UI components."""

import streamlit as st

from utils.calculations import budget_stats
from utils.constants import BUDGET_STATES, budget_state
from utils.formatting import format_currency


def render_budget_progress(total_spent: float, budget: float | None) -> None:
    """Render budget progress card."""
    stats = budget_stats(total_spent, budget)

    if stats["budget"] is None:
        st.markdown(
            '<div class="budget-card">'
            '<p class="budget-no-set">No budget set for this month. '
            "Set one in More → Monthly Budget.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
        return

    percent = min(stats["percent_used"], 100)
    state_key = budget_state(stats["percent_used"])
    state = BUDGET_STATES[state_key]
    fill_color = state["color"]
    display_percent = stats["percent_used"]

    remaining_text = format_currency(stats["remaining"])
    if stats["remaining"] < 0:
        remaining_text = f"{format_currency(abs(stats['remaining']))} over"

    st.markdown(
        f"""
        <div class="budget-card">
            <div class="budget-stats">
                <span><span class="budget-stat-value">{format_currency(stats['spent'])}</span> spent</span>
                <span><span class="budget-stat-value">{format_currency(stats['budget'])}</span> budget</span>
            </div>
            <div class="budget-progress-track">
                <div class="budget-progress-fill" style="width: {percent}%; background: {fill_color};"></div>
            </div>
            <div class="budget-stats">
                <span><span class="budget-stat-value">{remaining_text}</span> remaining</span>
                <span><span class="budget-stat-value">{display_percent:.0f}%</span> used</span>
            </div>
            <div class="budget-state-label" style="color: {fill_color};">{state['label']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
