"""Insights page — simple spending analytics."""

import streamlit as st
import plotly.express as px

from database import queries
from utils.calculations import (
    average_daily_spending,
    category_chart_data,
    daily_spending_trend,
    highest_spending_day,
    largest_expense,
    month_comparison,
    previous_month_year,
    total_spending,
)
from utils.formatting import (
    format_currency,
    format_date_long,
    render_empty_state,
    render_stat_card,
)
from utils.navigation import month_selector


def render() -> None:
    st.markdown("## Insights")

    month, year = month_selector("insights")

    expenses, error = queries.get_expenses(month=month, year=year)
    if error:
        st.error(error)
        return

    if not expenses:
        st.markdown(
            render_empty_state(
                "No data for this month.",
                "Add expenses to see insights.",
            ),
            unsafe_allow_html=True,
        )
        return

    total = total_spending(expenses)
    avg_daily = average_daily_spending(expenses, month, year)
    largest = largest_expense(expenses)
    highest_day = highest_spending_day(expenses)

    prev_month, prev_year = previous_month_year(month, year)
    prev_expenses, prev_error = queries.get_expenses(month=prev_month, year=prev_year)
    comparison = None
    if not prev_error:
        comparison = month_comparison(
            total,
            total_spending(prev_expenses),
            prev_month,
            prev_year,
        )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            render_stat_card("Average daily spending", f"{format_currency(avg_daily)} / day"),
            unsafe_allow_html=True,
        )
    with col2:
        if comparison:
            st.markdown(render_stat_card("vs last month", comparison), unsafe_allow_html=True)

    if largest:
        desc = largest.get("description") or largest["category"]
        st.markdown(
            render_stat_card(
                "Largest expense",
                f"{format_currency(largest['amount'])} - {desc}",
            ),
            unsafe_allow_html=True,
        )

    if highest_day:
        st.markdown(
            render_stat_card(
                "Highest spending day",
                f"{format_date_long(highest_day['date'])} - {format_currency(highest_day['amount'])}",
            ),
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-header">Spending by Category</div>', unsafe_allow_html=True)
    cat_df = category_chart_data(expenses)
    if not cat_df.empty:
        is_dark = st.session_state.get("dark_mode", False)
        bg_color = "#0f172a" if is_dark else "#ffffff"
        text_color = "#e2e8f0" if is_dark else "#111827"
        grid_color = "#334155" if is_dark else "#E5E7EB"
        palette = [
            "#4F81BD",
            "#5EC2D9",
            "#7CC7A3",
            "#E8D46A",
            "#E39C68",
            "#8B5CF6",
            "#F59E0B",
            "#E11D48",
        ]
        fig = px.pie(
            cat_df,
            values="amount",
            names="category",
            hole=0.52,
            color_discrete_sequence=palette,
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            height=260,
            width=360,
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            font=dict(color=text_color),
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            insidetextfont=dict(color="white", size=11),
            marker=dict(line=dict(color="#FFFFFF", width=2)),
            hovertemplate="<b>%{label}</b><br>Amount: ₹%{value:,.0f}<extra></extra>",
        )
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Daily Spending</div>', unsafe_allow_html=True)
    trend_df = daily_spending_trend(expenses)
    if not trend_df.empty:
        is_dark = st.session_state.get("dark_mode", False)
        bg_color = "#0f172a" if is_dark else "#ffffff"
        text_color = "#e2e8f0" if is_dark else "#111827"
        grid_color = "#334155" if is_dark else "#E5E7EB"
        min_amount = float(trend_df["amount"].min()) if not trend_df.empty else 0
        max_amount = float(trend_df["amount"].max()) if not trend_df.empty else 0
        if max_amount == min_amount:
            colors = ["#EF4444"] * len(trend_df)
        else:
            colors = []
            for value in trend_df["amount"]:
                ratio = (float(value) - min_amount) / (max_amount - min_amount)
                if ratio < 0.2:
                    colors.append("#FECACA")
                elif ratio < 0.4:
                    colors.append("#FCA5A5")
                elif ratio < 0.6:
                    colors.append("#F87171")
                elif ratio < 0.8:
                    colors.append("#EF4444")
                else:
                    colors.append("#B91C1C")

        fig = px.bar(
            trend_df,
            x="date",
            y="amount",
            labels={"date": "Date", "amount": "Amount (₹)"},
        )
        fig.update_traces(
            marker=dict(color=colors, line=dict(color="#FFFFFF", width=1.5), opacity=0.95),
            hovertemplate="<b>%{x}</b><br>Spent: ₹%{y:,.0f}<extra></extra>",
        )
        fig.update_layout(
            margin=dict(l=24, r=20, t=20, b=20),
            height=280,
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            xaxis_title="",
            yaxis_title="",
            xaxis=dict(
                showgrid=False,
                tickfont=dict(size=10, color=text_color),
                title_font=dict(color=text_color),
                linecolor=grid_color,
                tickcolor=text_color,
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=grid_color,
                zeroline=False,
                tickfont=dict(size=10, color=text_color),
                title_font=dict(color=text_color),
                linecolor=grid_color,
                tickcolor=text_color,
            ),
            bargap=0.35,
            showlegend=False,
            font=dict(color=text_color),
        )
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


render()
