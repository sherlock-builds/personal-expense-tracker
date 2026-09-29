"""Personal Expense Tracker — main entry point."""

import streamlit as st

from utils.navigation import (
    apply_theme_css,
    init_session_state,
    load_css,
    render_bottom_nav,
)

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed",
)

load_css()
init_session_state()
apply_theme_css()

home_page = st.Page("pages/home.py", title="Home", icon="🏠", default=True)
add_page = st.Page("pages/add_expense.py", title="Add Expense", icon="➕")
history_page = st.Page("pages/history.py", title="History", icon="📋")
insights_page = st.Page("pages/insights.py", title="Insights", icon="📊")
settings_page = st.Page("pages/settings.py", title="More", icon="⚙️")

pages = [home_page, add_page, history_page, insights_page, settings_page]
current_page = st.navigation(pages, position="hidden")

current_page.run()
render_bottom_nav()
