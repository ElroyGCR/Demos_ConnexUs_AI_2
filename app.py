import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# Constants
HOURS_PER_MONTH = 160
AI_RATE_OPTIONS = [18, 20, 22]

def calculate_costs(agents, human_rate, tax_pct, talk_pct, ai_rate):
    total_hours = agents * HOURS_PER_MONTH
    human_base = total_hours * human_rate
    human_tax = human_base * tax_pct
    human_total = human_base + human_tax
    required_ai = agents * talk_pct
    ai_total = required_ai * HOURS_PER_MONTH * ai_rate
    savings = human_total - ai_total

    return {
        "hours": total_hours,
        "human_base": human_base,
        "human_tax": human_tax,
        "human_total": human_total,
        "ai_total": ai_total,
        "required_ai": required_ai,
        "savings": savings,
    }

def main():
    st.title("Human Agents vs AI Agents ROI Calculator")

    # Sidebar inputs
    agents = st.sidebar.slider("Number of Agents", 1, 100, 15)
    human_rate = st.sidebar.slider("Agent Hourly Rate (USD)", 5.0, 50.0, 20.0)
    tax_pct = st.sidebar.slider("Taxes & Benefits (%)", 0, 100, 25) / 100.0
    talk_pct = st.sidebar.slider("Talk Utilization (%)", 0, 100, 40) / 100.0
    ai_rate = st.sidebar.select_slider("AI Hourly Rate (USD)", AI_RATE_OPTIONS, value=20)

    # Compute costs
    costs = calculate_costs(agents, human_rate, tax_pct, talk_pct, ai_rate)

    # Display key metrics
    st.metric("Total Monthly Hours", f"{int(costs['hours']):,}")
    st.metric("Human Agent Cost",     f"$ {costs['human_total']:,.0f}")
    st.metric("AI Agent Cost",        f"$ {costs['ai_total']:,.0f}")
    st.metric("Monthly Savings",      f"$ {costs['savings']:,.0f}")
    st.metric("Required AI Agents",   f"{costs['required_ai']:.1f}")

    # Prepare multi-period data
    months = [1, 6, 12, 18, 24, 36, 48, 60]
    df = pd.DataFrame([
        {
            "Period": f"{m}{' Month' if m == 1 else ' Months'}",
            "Human Cost": costs["human_total"] * m,
            "AI Cost":    costs["ai_total"] * m,
        }
        for m in months
    ])

    # Line chart
    chart = alt.Chart(df).transform_fold(
        ["Human Cost", "AI Cost"],
        as_=["Type", "Cost"]
    ).mark_line(point=True).encode(
        x="Period:N", y="Cost:Q", color="Type:N"
    ).properties(
        height=400, width=700
    )

    st.altair_chart(chart, use_container_width=True)

if __name__ == "__main__":
    main()
