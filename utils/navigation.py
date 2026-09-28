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
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True


def apply_theme_css() -> None:
    """Apply the current app theme across all pages."""
    is_dark = st.session_state.get("dark_mode", False)
    if is_dark:
        st.markdown(
            """
            <style>
            [data-testid="stAppViewContainer"] {
                background: #0f172a;
                color: #e2e8f0;
            }
            .block-container {
                background: #0f172a;
            }
            .summary-card,
            .stat-card,
            .expense-card,
            .budget-card,
            .stButton > button,
            .stSelectbox > div,
            .stTextInput > div,
            .stNumberInput > div,
            .stDateInput > div,
            .stTextArea > div,
            .stRadio > div,
            .stCheckbox > div,
            .stContainer,
            .stDataFrame,
            .stTabs,
            div[data-testid="stForm"],
            div[data-testid="stForm"] > div,
            [data-testid="stBaseInputContainer"],
            [data-testid="stBaseInputContainer"] > div {
                background: #111827 !important;
                border-color: #334155 !important;
                color: #e2e8f0 !important;
            }
            .total-spend,
            .total-spend-label,
            .stat-label,
            .stat-value,
            .stat-subtext,
            .expense-title,
            .expense-meta,
            .expense-amount,
            .category-label,
            .category-amount,
            .budget-stat-value,
            .empty-message,
            .empty-hint,
            .section-header,
            .settings-list-item,
            .history-item-header,
            .month-header,
            .stApp h1,
            .stApp h2,
            .stApp h3,
            .stApp p,
            .stApp span,
            .stApp div {
                color: #e2e8f0 !important;
            }
            .budget-progress-track,
            .category-bar-track,
            .stTextInput input,
            .stSelectbox input,
            .stDateInput input,
            .stNumberInput input,
            .stTextArea textarea,
            .stTextInput > div > div,
            .stSelectbox > div > div,
            div[data-testid="stForm"] input,
            div[data-testid="stForm"] textarea,
            div[data-testid="stForm"] select,
            [data-testid="stBaseInputContainer"],
            [data-testid="stBaseInputContainer"] > div,
            [data-testid="stBaseInputContainer"] input,
            [data-testid="stBaseInputContainer"] textarea,
            [data-testid="stBaseInputContainer"] select,
            [data-testid="stTextInputRootElement"],
            [data-testid="stTextInputRootElement"] input,
            [data-testid="stNumberInputContainer"],
            [data-testid="stNumberInputContainer"] input,
            [data-testid="stNumberInputField"],
            [data-testid="stDateInputField"],
            [data-testid="stDateInputField"] input,
            [data-testid="stSelectbox"] input,
            [data-testid="stSelectbox"] [role="group"],
            [data-testid="stSelectbox"] [role="combobox"],
            [data-testid="stTextInputField"] {
                background: #0f172a !important;
                color: #e2e8f0 !important;
                border-color: #475569 !important;
            }
            [data-testid="stBaseInputContainer"],
            [data-testid="stTextInputRootElement"],
            [data-testid="stNumberInputContainer"],
            [data-testid="stDateInputField"],
            [data-testid="stSelectbox"] [role="group"],
            [data-testid="stSelectbox"] [role="combobox"],
            [data-testid="stTextInputField"],
            [data-testid="stNumberInputField"] {
                border: 1px solid #475569 !important;
                border-radius: 0.75rem !important;
                box-shadow: none !important;
                background: #0f172a !important;
            }
            [data-testid="stBaseInputContainer"] > div,
            [data-testid="stBaseInputContainer"] > div > div,
            [data-testid="stTextInputRootElement"] > div,
            [data-testid="stTextInputRootElement"] > div > div,
            [data-testid="stNumberInputContainer"] > div,
            [data-testid="stNumberInputContainer"] > div > div,
            [data-testid="stDateInputField"] > div,
            [data-testid="stDateInputField"] > div > div,
            [data-testid="stSelectbox"] [role="group"] > div,
            [data-testid="stSelectbox"] [role="group"] > div > div {
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
            }
            .stTextInput input::placeholder,
            .stTextArea textarea::placeholder,
            .stNumberInput input::placeholder,
            .stDateInput input::placeholder,
            .stSelectbox select::placeholder,
            input::placeholder,
            textarea::placeholder,
            select::placeholder {
                color: #dbeafe !important;
                opacity: 1 !important;
            }
            .stTextInput input::-webkit-input-placeholder,
            .stTextArea textarea::-webkit-input-placeholder,
            .stNumberInput input::-webkit-input-placeholder,
            .stDateInput input::-webkit-input-placeholder,
            input::-webkit-input-placeholder,
            textarea::-webkit-input-placeholder,
            select::-webkit-input-placeholder {
                color: #dbeafe !important;
                opacity: 1 !important;
            }
            .stTextInput input::-moz-placeholder,
            .stTextArea textarea::-moz-placeholder,
            .stNumberInput input::-moz-placeholder,
            .stDateInput input::-moz-placeholder,
            input::-moz-placeholder,
            textarea::-moz-placeholder,
            select::-moz-placeholder {
                color: #dbeafe !important;
                opacity: 1 !important;
            }
            .stTextInput input:-ms-input-placeholder,
            .stTextArea textarea:-ms-input-placeholder,
            .stNumberInput input:-ms-input-placeholder,
            .stDateInput input:-ms-input-placeholder,
            input:-ms-input-placeholder,
            textarea:-ms-input-placeholder,
            select:-ms-input-placeholder {
                color: #dbeafe !important;
                opacity: 1 !important;
            }
            .stTextInput input,
            .stTextArea textarea,
            .stNumberInput input,
            .stDateInput input,
            .stSelectbox select,
            div[data-testid="stForm"] input,
            div[data-testid="stForm"] textarea,
            div[data-testid="stForm"] select,
            input,
            textarea,
            select {
                -webkit-text-fill-color: #e2e8f0 !important;
                color: #e2e8f0 !important;
            }
            button[data-testid="stNumberInputStepUp"],
            button[data-testid="stNumberInputStepDown"],
            button[data-testid="stNumberInputStepUp"] svg,
            button[data-testid="stNumberInputStepDown"] svg,
            button[data-testid="stNumberInputStepUp"] path,
            button[data-testid="stNumberInputStepDown"] path,
            button[aria-label="Open"],
            button[aria-label="Open"] svg,
            button[aria-label="Open"] path,
            [data-testid="stSelectbox"] button[aria-label="Open"],
            [data-testid="stSelectbox"] button[aria-label="Open"] svg,
            [data-testid="stSelectbox"] button[aria-label="Open"] path {
                color: #e2e8f0 !important;
                fill: #e2e8f0 !important;
                stroke: #e2e8f0 !important;
                border-color: #e2e8f0 !important;
                background: transparent !important;
            }
            button[data-testid="stNumberInputStepUp"] > svg,
            button[data-testid="stNumberInputStepDown"] > svg,
            button[aria-label="Open"] > svg,
            button[aria-label="Open"] > svg > path,
            button[data-testid="stNumberInputStepUp"] > svg > path,
            button[data-testid="stNumberInputStepDown"] > svg > path {
                color: #e2e8f0 !important;
                fill: #e2e8f0 !important;
                stroke: #e2e8f0 !important;
            }
            div[data-testid="stForm"] {
                background: #0f172a !important;
                border: 1px solid #334155 !important;
                border-radius: 1rem !important;
                padding: 0.25rem 0 !important;
            }
            div[data-testid="stForm"] > div {
                background: transparent !important;
            }
            .stHorizontalBlock:has(a[href]) {
                background: #111827 !important;
                border-top: 1px solid #334155 !important;
            }
            .stHorizontalBlock:has(a[href]) > .stColumn .stPageLink,
            .stHorizontalBlock:has(a[href]) > .stColumn a[href] {
                color: #cbd5e1 !important;
            }
            .stHorizontalBlock:has(a[href]) > .stColumn .stPageLink[aria-current="page"],
            .stHorizontalBlock:has(a[href]) > .stColumn a[href][aria-current="page"] {
                background: #1e293b !important;
                color: #f8fafc !important;
            }
            div[data-testid="stVerticalBlockBorderWrapper"] {
                border-color: #334155 !important;
                background: #111827 !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <style>
            [data-testid="stAppViewContainer"] {
                background: #ffffff;
                color: #111827;
            }
            .block-container {
                background: #ffffff;
            }
            div[data-testid="stBaseInputContainer"],
            div[data-testid="stBaseInputContainer"] > div,
            .stTextInput > div,
            .stTextInput > div > div,
            .stSelectbox > div,
            .stSelectbox > div > div,
            .stDateInput > div,
            .stDateInput > div > div,
            .stNumberInput > div,
            .stNumberInput > div > div,
            .stTextArea > div,
            .stTextArea > div > div,
            div[data-baseweb="select"],
            div[data-baseweb="select"] > div,
            input,
            textarea,
            select {
                border: 1px solid #d1d5db !important;
                border-radius: 0.75rem !important;
                background: #ffffff !important;
                box-shadow: none !important;
                color: #111827 !important;
                box-sizing: border-box !important;
            }
            .stTextInput input::placeholder,
            .stTextArea textarea::placeholder,
            .stNumberInput input::placeholder,
            .stDateInput input::placeholder,
            .stSelectbox select::placeholder,
            input::placeholder,
            textarea::placeholder,
            select::placeholder {
                color: #64748b !important;
                opacity: 1 !important;
            }
            .stApp label,
            .stApp .stTextInput label,
            .stApp .stSelectbox label,
            .stApp .stDateInput label,
            .stApp .stNumberInput label,
            .stApp .stTextArea label {
                color: #111827 !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


def render_theme_toggle() -> None:
    """Render a global theme toggle on every page."""
    st.toggle("Dark mode", key="dark_mode")


def render_bottom_nav() -> None:
    """Render fixed app navigation."""
    nav_items = [
        ("Home", "pages/home.py", "🏠"),
        ("Add", "pages/add_expense.py", "➕"),
        ("History", "pages/history.py", "📋"),
        ("Insights", "pages/insights.py", "📊"),
        ("More", "pages/settings.py", "⚙️"),
    ]

    with st.container(key="bottom_nav"):
        cols = st.columns(5, gap="xxsmall", wrap=False)

        for col, (label, page, icon) in zip(cols, nav_items):
            with col:
                st.page_link(
                    page,
                    label=label,
                    icon=icon,
                    use_container_width=True,
                )


def month_selector(key_prefix: str = "global") -> tuple[int, int]:
    """Render month/year selector and return selected values."""
    from utils.constants import MONTH_NAMES

    month_index = st.session_state.selected_month - 1

    col1, col2, col3 = st.columns([1, 4, 1], gap="small", vertical_alignment="center")
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
            f'<div class="month-header" style="text-align:center;margin:0;white-space:nowrap;">'
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
