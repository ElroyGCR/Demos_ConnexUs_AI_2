import sys
import types
# Stub out missing micropip module to prevent import errors in sandbox
sys.modules['micropip'] = types.ModuleType('micropip')

import streamlit as st

# ─── Page Config ───────────────────────────────────────
st.set_page_config(page_title="AI Savings Calculator", layout="wide", page_icon="💰")

# ─── Calculation Logic ─────────────────────────────────
def calculate_metrics(
    agents, human_rate, burden_pct, talk_pct, hours_per_month,
    subscription, ai_cost_min, ai_speed, automation_pct,
    integration_fee, include_indirect, hr_pct
):
    # Validate ai_speed
    if ai_speed <= 0:
        st.error("AI Speed Factor must be greater than zero. Using 1 as fallback.")
        ai_speed = 1

    # Baseline human cost including benefits
    burden_mul = 1 + burden_pct / 100
    baseline = agents * hours_per_month * human_rate * burden_mul

    # Human residual cost after AI handles part
    residual = baseline * (1 - automation_pct / 100)

    # AI variable cost via minutes and speed factor
    talk_hours_total = agents * hours_per_month * (talk_pct / 100)
    ai_hours = talk_hours_total * (automation_pct / 100)
    minutes_handled = ai_hours * 60
    raw_ai_cost = minutes_handled * ai_cost_min
    ai_variable = raw_ai_cost / ai_speed

    # Net savings
    ai_enabled_cost = residual + ai_variable + subscription
    net_savings = baseline - ai_enabled_cost

    # Indirect & strategic savings
    indirect = 0.0
    strategic = 0.0
    if include_indirect:
        indirect = baseline * (1 - talk_pct / 100) * (automation_pct / 100) * ai_speed
        strategic = indirect * (hr_pct / 100)
    total_value = net_savings + indirect + strategic

    # Return and payback
    ai_spend = subscription + ai_variable
    return_per_dollar = total_value / ai_spend if ai_spend > 0 else 0.0
    payback_months = integration_fee / total_value if total_value > 0 else float('inf')

    return net_savings, return_per_dollar, payback_months

# ─── App Layout ────────────────────────────────────────
st.title("AI Savings Calculator")

input_col, result_col = st.columns([2, 3])

with input_col:
    st.header("Your Information")
    agents = st.number_input("Number of People", min_value=0, value=10, step=1)
    human_rate = st.number_input("Pay Per Hour ($)", min_value=0.0, value=20.0, step=0.01)
    burden_pct = st.slider("Extra Cost for Benefits (%)", 0, 100, 30)
    hours_per_month = st.number_input("Hours Worked Each Month", min_value=0.0, value=160.0, step=0.1)
    talk_pct = st.slider("Percent of Time Helping Customers (%)", 0, 100, 50)

    st.header("AI Costs")
    subscription = st.number_input("Monthly AI Fee ($)", min_value=0.0, value=1000.0, step=0.01)
    ai_cost_min = st.number_input("AI Talk Cost (per min $)", min_value=0.0, value=0.20, step=0.01)
    ai_speed = st.number_input(
        "AI Speed Factor (times faster AI works than a person)",
        min_value=0.1, value=2.0, step=0.1
    )
    automation_pct = st.slider("Goal: How Much AI Will Help (%)", 0, 100, 40)
    integration_fee = st.number_input("One-Time Setup Cost ($)", min_value=0.0, value=10000.0, step=1.0)

    include_indirect = st.checkbox("Include Extra Savings (fewer mistakes, happier staff)", value=True)
    hr_pct = st.slider("Extra Savings Percent (%)", 0, 100, 10) if include_indirect else 0

# Calculate metrics
net_savings, return_per_dollar, payback_months = calculate_metrics(
    agents, human_rate, burden_pct, talk_pct, hours_per_month,
    subscription, ai_cost_min, ai_speed, automation_pct,
    integration_fee, include_indirect, hr_pct
)

# Display banner
banner_html = f"""
<div style='background-color: #E0F7FA; padding: 20px; border-radius: 10px; text-align: center;'>
  <h2>You’ll save <span style='color:#2E7D32;'>${net_savings:,.0f}</span> each month!</h2>
  <p>For every $1 you spend on AI, you get {return_per_dollar:,.2f} back.</p>
  <p>You’ll get your setup fee back in {('N/A' if payback_months==float('inf') else f"{payback_months:,.1f}")} months.</p>
</div>
"""
result_col.markdown(banner_html, unsafe_allow_html=True)

# Display key results in metrics
metrics_col1, metrics_col2, metrics_col3 = result_col.columns(3)
metrics_col1.metric("Money You Keep Each Month", f"${net_savings:,.0f}")
metrics_col2.metric("Return per Dollar", f"{return_per_dollar:,.2f}")
payback_display = "N/A" if payback_months==float('inf') else f"{payback_months:,.1f} mo"
metrics_col3.metric("Months to Pay Back Setup", payback_display)
