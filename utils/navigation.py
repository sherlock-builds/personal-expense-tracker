"""Shared navigation and styling helpers."""

from pathlib import Path

import streamlit as st


def load_css() -> None:
    """Inject custom CSS from assets/style.css."""
    css_path = Path(__file__).parent.parent / "assets" / "style.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def init_session_state() -> None:
    """Initialize shared session state variables."""
    today = __import__("datetime").date.today()
    if "selected_month" not in st.session_state:
        st.session_state.selected_month = today.month
    if "selected_year" not in st.session_state:
        st.session_state.selected_year = today.year


def render_bottom_nav() -> None:
    """Render fixed bottom (mobile) / top (desktop) navigation bar."""
    nav_items = [
        ("Home", "pages/home.py", "🏠"),
        ("Add", "pages/add_expense.py", "➕"),
        ("History", "pages/history.py", "📋"),
        ("Insights", "pages/insights.py", "📊"),
        ("More", "pages/settings.py", "⚙️"),
    ]

    with st.container():
        st.markdown('<div class="bottom-nav-container">', unsafe_allow_html=True)
        cols = st.columns(5)
        for col, (label, page, icon) in zip(cols, nav_items):
            with col:
                st.page_link(page, label=label, icon=icon, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


def month_selector(key_prefix: str = "global") -> tuple[int, int]:
    """Render month/year selector and return selected values."""
    from utils.constants import MONTH_NAMES

    month_index = st.session_state.selected_month - 1

    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("◀", key=f"{key_prefix}_prev_month"):
            if st.session_state.selected_month == 1:
                st.session_state.selected_month = 12
                st.session_state.selected_year -= 1
            else:
                st.session_state.selected_month -= 1
            st.rerun()
    with col2:
        st.markdown(
            f'<div class="month-header" style="text-align:center;margin:0;">'
            f'{MONTH_NAMES[month_index]} {st.session_state.selected_year}</div>',
            unsafe_allow_html=True,
        )
    with col3:
        if st.button("▶", key=f"{key_prefix}_next_month"):
            if st.session_state.selected_month == 12:
                st.session_state.selected_month = 1
                st.session_state.selected_year += 1
            else:
                st.session_state.selected_month += 1
            st.rerun()

    return st.session_state.selected_month, st.session_state.selected_year
