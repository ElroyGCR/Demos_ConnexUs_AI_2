# Streamlit AI Savings Calculator
# -----------------------------------
# This script requires Streamlit. Make sure you have it installed in your environment:
#     pip install streamlit

import sys
import os
import math

# Attempt to import Streamlit
try:
    import streamlit as st
except ImportError:
    sys.exit(
        "Error: Streamlit module not found.\n"
        "Please install Streamlit by running 'pip install streamlit' in your environment."
    )

# ─── Page Setup ────────────────────────────────────────
# IMPORTANT: st.set_page_config must be the first Streamlit command
st.set_page_config(page_title="AI Savings Calculator", layout="wide", page_icon="💰")

# Get branding inputs (these can't affect page config now)
brand_title = st.sidebar.text_input("App Title", value="AI Savings Calculator")
brand_icon = st.sidebar.text_input("App Icon (emoji)", value="💰")

# ─── Calculation Logic ─────────────────────────────────

def calculate_metrics(
    agents: int,
    human_rate: float,
    burden_pct: float,
    talk_pct: float,
    hours_per_month: float,
    subscription: float,
    automation_pct: float,
    integration_fee: float,
    include_indirect: bool,
    hr_pct: float,
    ai_efficiency_factor: float = 2.0
) -> dict:
    """
    Compute AI savings metrics based on inputs.
    Returns a dict with keys for all core metrics.
    """
    burden_mul = 1 + burden_pct / 100
    baseline = agents * hours_per_month * human_rate * burden_mul
    productive = baseline * (talk_pct / 100)
    unproductive = baseline * (1 - talk_pct / 100)
    residual = baseline * (1 - automation_pct / 100)
    ai_variable = (productive * (automation_pct / 100)) / ai_efficiency_factor
    ai_enabled = residual + ai_variable + subscription
    net_savings = baseline - ai_enabled
    monthly_eff = (net_savings / baseline) * 100 if baseline > 0 else float('nan')
    indirect = unproductive * (automation_pct / 100) * ai_efficiency_factor if include_indirect else 0.0
    strategic = indirect * (hr_pct / 100) if include_indirect else 0.0
    total_value = net_savings + indirect + strategic
    roi_integ_mo = (total_value / integration_fee) * 100 if integration_fee > 0 else float('nan')
    roi_integ_yr = roi_integ_mo * 12 if math.isfinite(roi_integ_mo) else float('nan')
    payback_integ = integration_fee / total_value if total_value > 0 else float('nan')
    roi_prod_mo = (total_value / baseline) * 100 if baseline > 0 else float('nan')
    payback_prod = baseline / total_value if total_value > 0 else float('nan')
    ai_spend = subscription + ai_variable
    return_per = total_value / ai_spend if ai_spend > 0 else float('nan')

    return {
        'burden_mul': burden_mul,
        'baseline_human_cost': baseline,
        'productive_cost': productive,
        'unproductive_cost': unproductive,
        'residual_human_cost': residual,
        'ai_variable_cost': ai_variable,
        'ai_enabled_cost': ai_enabled,
        'net_savings': net_savings,
        'monthly_cost_efficiency': monthly_eff,
        'indirect_savings': indirect,
        'strategic_savings': strategic,
        'total_value': total_value,
        'roi_integ_mo': roi_integ_mo,
        'roi_integ_yr': roi_integ_yr,
        'payback_mo_integ': payback_integ,
        'roi_prod_mo': roi_prod_mo,
        'payback_mo_prod': payback_prod,
        'ai_spend': ai_spend,
        'return_per_dollar': return_per,
    }

# ─── Banner Rendering ──────────────────────────────────

def render_banner(metrics: dict):
    """
    Display the main savings banner with checks for invalid values.
    """
    net = metrics.get('net_savings', float('nan'))
    ret = metrics.get('return_per_dollar', float('nan'))
    payback = metrics.get('payback_mo_integ', float('nan'))

    banner_net = f"${{int(net):,}}" if math.isfinite(net) else "N/A"
    banner_ret = f"{ret:,.2f}" if math.isfinite(ret) else "N/A"
    banner_pay = f"{payback:.1f}" if math.isfinite(payback) else "N/A"

    st.markdown(f"""
    <div class='banner'>
      <h2>You'll save <span style='color:#2E7D32;'>{banner_net}</span> each month!</h2>
      <p>For every $1 you spend on AI, you get {banner_ret} back.</p>
      <p>You'll get your setup money back in {banner_pay} months.</p>
    </div>
    """, unsafe_allow_html=True)

# ─── Styles ────────────────────────────────────────────
st.markdown("""
<style>
  .banner { background-color: #E0F7FA; padding: 20px; border-radius: 10px; text-align: center; }
  .result-card { background-color: #F1F8E9; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
  .tooltip { cursor: help; color: #0288D1; margin-left: 5px; }
</style>
""", unsafe_allow_html=True)

# ─── Example Story ─────────────────────────────────────
st.markdown("""
> **Meet Alex.** Alex has 10 people who each work 160 hours a month at $20/hour. By letting AI help with 40% of the work,
> Alex keeps an extra $8,000 each month and gets the $10,000 setup fee back in just 3 months!
""")
st.markdown("---")

# ─── Inputs & Results Layout ─────────────────────────────
input_col, result_col = st.columns([1, 1])
with input_col:
    st.header("Your Information")
    agents = st.number_input("Number of People", min_value=1, value=10, step=1)
    human_rate = st.number_input("Pay Per Hour", min_value=1.0, value=20.0, step=1.0)
    burden_pct = st.slider("Extra Cost for Benefits (%)", 0, 100, 30, step=5)
    hours_per_month = st.number_input("Hours Worked Each Month", min_value=1.0, value=160.0, step=1.0)
    talk_pct = st.slider("Percent of Time Helping Customers", 0, 100, 50, step=5)

    st.subheader("AI Costs")
    subscription = st.number_input("Monthly AI Fee ($)", min_value=0.0, value=1000.0, step=50.0)
    ai_cost_min = st.number_input("AI Talk Cost (per min)", min_value=0.01, value=0.20, step=0.01)
    automation_pct = st.slider("Goal: How Much AI Will Help (%)", 0, 100, 40, step=5)
    integration_fee = st.number_input("One-Time Setup Cost ($)", min_value=0.0, value=10000.0, step=500.0)

    include_indirect = st.checkbox("Include Extra Savings (fewer mistakes, happier staff)", value=True)
    hr_pct = st.slider("Extra Savings: What percent to count?", 0, 100, 10, step=5) if include_indirect else 0

with result_col:
    st.header("Your Results")
    metrics = calculate_metrics(
        agents=agents,
        human_rate=human_rate,
        burden_pct=burden_pct,
        talk_pct=talk_pct,
        hours_per_month=hours_per_month,
        subscription=subscription,
        automation_pct=automation_pct,
        integration_fee=integration_fee,
        include_indirect=include_indirect,
        hr_pct=hr_pct,
    )

    # Render banner via helper
    render_banner(metrics)

    # Detailed cards
    for label, key, tooltip in [
        ("Money You Keep Each Month", 'net_savings',
         "This is how much extra cash stays in your bank every month."),
        ("Return per Dollar", 'return_per_dollar',
         "For every dollar you pay AI, you get this many dollars back in savings."),
        ("Months to Pay Back Setup", 'payback_mo_integ',
         "How many months until your one-time fee is earned back."),
    ]:
        value = metrics.get(key, float('nan'))
        display = f"{value:,.2f}" if isinstance(value, float) and math.isfinite(value) else (f"{int(value):,}" if isinstance(value, (int, float)) and math.isfinite(value) else "N/A")
        st.markdown(f"""
        <div class='result-card'>
          <b>{label}</b> <span class='tooltip' title='{tooltip}'>ℹ️</span><br>
          <span style='font-size:24px;'>{display}</span>
        </div>
        """, unsafe_allow_html=True)

# ─── Unit Tests ─────────────────────────────────────
if not os.getenv('STREAMLIT_RUN'):
    def _almost_equal(a, b, tol=1e-6): return abs((a or 0) - (b or 0)) < tol
    test_inputs = dict(
        agents=10,
        human_rate=20.0,
        burden_pct=30,
        talk_pct=50,
        hours_per_month=160.0,
        subscription=1000.0,
        automation_pct=40,
        integration_fee=10000.0,
        include_indirect=True,
        hr_pct=10,
    )
    expected = calculate_metrics(**test_inputs)
    got = calculate_metrics(**test_inputs)
    assert set(got.keys()) == set(expected.keys()), "Mismatch in metric keys"
    for k in expected:
        assert _almost_equal(got[k], expected[k]), f"Metric {k} - expected {expected[k]}, got {got[k]}"
    print("All unit tests passed!")
