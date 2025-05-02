import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from io import BytesIO
import base64

# --- Page Setup ---
st.set_page_config(page_title="ConnexUs.AI Calculator", page_icon="favicon-32x32.png", layout="wide")

# --- Favicon Injection (Base64 Embedded) ---
def load_favicon_base64(path="favicon-32x32.png"):
    try:
        img = Image.open(path)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")
    except Exception:
        return None

favicon_b64 = load_favicon_base64()
if favicon_b64:
    st.markdown(
        f"""
        <link rel="icon" type="image/png" sizes="32x32" href="data:image/png;base64,{favicon_b64}">
        """,
        unsafe_allow_html=True
    )

# --- Theme-safe Global Styling ---
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 0rem !important;
    }
    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Watermark Setup ---
def load_watermark_base64(path="connexus_logo_watermark.png"):
    try:
        with open(path, "rb") as f:
            img = Image.open(f)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            return base64.b64encode(buffer.getvalue()).decode("utf-8")
    except:
        return None

watermark_b64 = load_watermark_base64()
if watermark_b64:
    st.markdown(
        f"""
        <style>
        .watermark {{
            position: fixed;
            top: 80px;
            left: calc(540px + 30%);
            transform: translateX(-50%);
            height: 800px;
            width: 850px;
            z-index: 0;
            pointer-events: none;
            background-image: url("data:image/png;base64,{watermark_b64}");
            background-repeat: no-repeat;
            background-position: center center;
            background-size: contain;
            opacity: 0.15;
        }}
        </style>
        <div class="watermark"></div>
        """,
        unsafe_allow_html=True
    )

# --- Title ---
st.markdown("""
    <div style='padding-top: 0rem;'>
        <h1 style='font-size: 2.4rem; font-weight: 800; margin-bottom: 1.5rem;'>ConnexUS AI ROI Calculator</h1>
        <hr style='margin-top: -1rem; margin-bottom: 1rem;'>
    </div>
""", unsafe_allow_html=True)

# Make background of Plotly graphs transparent
# This needs to be added wherever you define a chart layout:
# Example:
# fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

# Global layout setting for all Plotly charts
TRANSPARENT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# Now whenever you create a figure:
# fig.update_layout(**TRANSPARENT_LAYOUT)

def metric_block(label, value, color="#00FFAA", border="#00FFAA", prefix="", suffix=""):
    return f"""
    <div style='
        background-color: #111;
        border: 2px solid {border};
        border-radius: 12px;
        padding: 15px;
        width: fit-content;
        margin-bottom: 25px;
    '>
        <div style='color: white; font-size: 16px; margin-bottom: 5px;'>{label}</div>
        <div style='color: {color}; font-size: 36px; font-weight: bold;'>{prefix}{value:,.1f}{suffix}</div>
    </div>
    """
    
def caption(text):
    return f"<div style='color: white; font-size: 15px; margin-bottom: 10px;'>{text}</div>"

# Load logo
logo = Image.open("connexus_logo.png")

# --- SIDEBAR INPUTS ---
st.sidebar.image(logo, use_container_width=True)
st.sidebar.header("📊 Input Your Call Center Data")

# Revenue & Volume
st.sidebar.subheader("📈 Revenue & Volume")
monthly_revenue   = st.sidebar.number_input("Monthly Revenue ($)", value=250000, step=10000)
weekly_interactions = st.sidebar.number_input("Weekly Interactions", value=10000, step=100)
aht             = st.sidebar.slider("Average Handle Time (minutes)", 1, 20, 6)

# Workforce & Agent Metrics
st.sidebar.subheader("👥 Workforce & Agent Metrics")
agents          = st.sidebar.slider("Agents (FTE)", 1, 100, 25)
hourly_cost     = st.sidebar.slider("Agent Hourly Cost ($)", 10.0, 60.0, 15.0)
hours_per_week  = st.sidebar.slider("Weekly Hours per Agent", 35, 45, 40)
shift_hours     = st.sidebar.number_input("Shift Length (hours)", value=8.5, step=0.5)

# Business Impact Assumptions
st.sidebar.subheader("💼 Business Impact Assumptions")
production_percent = st.sidebar.number_input("Production Improvement (%)", value=25.0, step=0.1)
upsell_percent     = st.sidebar.number_input("Upsell Improvement (%)", value=10.0, step=0.1)

# AI Cost Inputs
st.sidebar.markdown("---")
st.sidebar.subheader("🤖 AI Cost Inputs")
automation       = st.sidebar.slider("AI Automation % Target", 0, 100, 50)
subscription      = st.sidebar.number_input("AI Monthly Subscription ($)", value=2000, step=100)
integration       = st.sidebar.number_input("One-time Integration Fee ($)", value=15000, step=1000)
ai_cost_per_min  = st.sidebar.number_input("AI Cost per Minute ($)", value=0.18, step=0.01)

# ROI Calculation Toggles
st.sidebar.markdown("---")
use_indirects    = st.sidebar.checkbox("Include Indirect Value in ROI Calculation", value=True)

# --- MAIN LAYOUT ---
st.markdown("<hr style='margin-top: -1rem; margin-bottom: 1rem;'>", unsafe_allow_html=True)

# --- 1. Total Monthly Workload ---
monthly_minutes = weekly_interactions * aht * 4.33

# --- 2. AI vs Residual Human Cost ---
ai_minutes       = (automation / 100) * monthly_minutes
residual_minutes = monthly_minutes - ai_minutes

# AI spend
ai_cost         = ai_minutes * ai_cost_per_min

# Residual human labor after automation, with fully-loaded multiplier
fully_loaded_multiplier = 1.222431
residual_cost    = (residual_minutes / 60) * hourly_cost * fully_loaded_multiplier

ai_enabled_cost      = ai_cost + residual_cost + subscription
# Cost excluding residual labor (pure AI spend + subscription)
total_ai_monthly_cost  = ai_cost + subscription

# --- 3. Indirect Value (Production & Upsell) ---
production_multiplier = production_percent / 100
upsell_multiplier     = upsell_percent / 100

# Convert saved minutes to dollar savings for production
production_minutes_saved = monthly_minutes * production_multiplier
production_hours_saved   = production_minutes_saved / 60
production_dollar_savings = production_hours_saved * hourly_cost * fully_loaded_multiplier

# Upsell tied to incremental revenue lift\_dollar_savings = monthly_revenue * upsell_multiplier
upsell_dollar_savings   = monthly_revenue * upsell_multiplier

# Total indirect savings in $ 
indirect_savings = production_dollar_savings + upsell_dollar_savings

total_monthly_value = (ai_enabled_cost := ai_enabled_cost)  # to preserve ai_enabled_cost name
net_savings           = None  # placeholder below

# --- 4. Baseline Human Cost Calculation ---
agent_monthly_hours = hours_per_week * 4.33
minutes_per_agent   = agent_monthly_hours * 60
required_agents     = monthly_minutes / minutes_per_agent
effective_agents   = max(agents, required_agents)

base_labor_cost     = effective_agents * agent_monthly_hours * hourly_cost
baseline_human_cost = base_labor_cost * fully_loaded_multiplier

# --- 5. Net Direct Savings ---
net_savings         = baseline_human_cost - ai_enabled_cost

# --- 6. ROI Value Basis (Direct + Optional Indirect + HR) ---
value_basis = net_savings
if use_indirects:
    value_basis += indirect_savings

# Placeholder for strategic (HR) impact; will be added later if toggled
strategic_total = 0

# --- 7. ROI & Payback on Operating Cost ---
roi_percent          = (value_basis / ai_enabled_cost) * 100 if ai_enabled_cost > 0 else 0
annual_roi_percent   = roi_percent * 12
payback_days         = (integration / value_basis) * 30 if value_basis > 0 else float('inf')

# --- 8. ROI vs Investment (Integration) ---
annual_net_savings    = total_monthly_value * 12
investment_roi       = ((annual_net_savings - integration) / integration) * 100 if integration > 0 else 0
investment_payback_months = (integration / annual_net_savings) * 12 if annual_net_savings > 0 else float('inf')

dollar_saved_per_ai_dollar = (value_basis / total_ai_monthly_cost) if total_ai_monthly_cost > 0 else 0

# --- 9. Build the Streamlit UI ---
# Core Financial Metrics
st.markdown("## 📊 Core Financial Metrics (Operating Basis)")
st.markdown(caption("These values reflect cost savings compared to your human-only baseline."), unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(metric_block("💰 Net Monthly Savings", net_savings, prefix="$"), unsafe_allow_html=True)
with col2:
    st.markdown(metric_block("🧾 Break-even Period", payback_days, suffix=" days"), unsafe_allow_html=True)
with col3:
    st.markdown(metric_block("📈 ROI on Operating Cost (Monthly)", roi_percent, suffix="%"), unsafe_allow_html=True)
with col4:
    st.markdown(metric_block("📈 ROI on Operating Cost (Annual)", annual_roi_percent, suffix="%"), unsafe_allow_html=True)

# AI Investment Impact
st.markdown("## 💡 AI Investment Impact")
st.markdown(caption("Shows how much value is returned for every dollar spent on AI — includes cost savings and indirect gains."), unsafe_allow_html=True)

st.markdown(
    f"""
    <div style='
        background-color: #111;
        border: 2px solid #00FFAA;
        border-radius: 12px;
        padding: 20px 30px;
        margin-top: 10px;
        margin-bottom: 20px;
        font-size: 30px;
        font-weight: 500;
        color: white;
        text-align: center;
    '>
        For every <span style='color:#FFD700; font-size: 46px; font-weight:800;'>$1</span> you invest in AI, you save:
        <span style='color:#00FFAA; font-size: 50px; font-weight:900;'>${dollar_saved_per_ai_dollar:,.2f}</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("## 💸 Monthly Cost Efficiency")
st.markdown(
    """
    <div style='color: white; font-size: 15px; margin-top: -10px; margin-bottom: 15px;'>
        This shows how much your monthly costs drop compared to a fully human-run operation.
    </div>
    """,
    unsafe_allow_html=True
)

# Monthly Cost Efficiency\st.markdown("### 💸 Monthly Cost Efficiency")
st.markdown(f"""
    <div style='
        background-color: #111;
        border: 2px solid #00FFAA;
        border-radius: 12px;
        padding: 15px;
        width: fit-content;
        margin-bottom: 25px;
    '>
        <div style='color: #00FFAA; font-size: 36px; font-weight: bold;'>
            {(net_savings / baseline_human_cost * 100):.2f}%
        </div>
    </div>
""", unsafe_allow_html=True)

# ROI & Break-even (Investment)
st.markdown("## 💼 ROI & Break-even Based on Investment")
st.markdown(
    """
    <div style='color: white; font-size: 15px; margin-top: -10px; margin-bottom: 20px;'>
        This section measures ROI compared to your up‑front investment (integration cost).<br>
        <strong>Investment ROI (%)</strong> calculates your return over the course of a year.<br>
        <strong>Payback Period (Months)</strong> estimates how many months it takes to recoup initial setup costs.
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    inv_fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=investment_roi,
        delta={'reference': 100},
        # Removed hardcoded font size for dynamic scaling
        title={'text': 'Investment ROI (%)', 'font': {'color': 'white'}},
        gauge={'axis': {'range': [0, 8000]}}
    ))
    st.plotly_chart(inv_fig, use_container_width=True)

with col2:
    pay_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=investment_payback_months,
        # Also removed font size for responsive behavior
        title={'text': "Payback Period (Months)", 'font': {'color': 'white'}},
        gauge={
            'axis': {'range': [0, 18]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 7], 'color': "lightgreen"},
                {'range': [7, 12], 'color': "yellow"},
                {'range': [12, 18], 'color': "tomato"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'value': 15}
        }
    ))
    st.plotly_chart(pay_fig, use_container_width=True)

# Donut Chart: AI Cost Composition
st.markdown("## 🍩 AI Cost Composition")
st.markdown(
    """
    <div style='color: white; font-size: 15px; margin-top: -10px; margin-bottom: 20px;'>
        This chart visualizes the composition of your AI-enabled monthly operating cost.
        <br>It breaks down how much is spent on AI usage, remaining labor, and platform subscription —
        helping you see where your new cost structure lies.
    </div>
    """,
    unsafe_allow_html=True
)

donut_fig = go.Figure(data=[go.Pie(
    labels=["AI Usage", "Residual Labor", "Subscription"],
    values=[ai_cost, residual_cost, subscription],
    hole=0.5,
    textinfo="label+percent+value",
    textfont=dict(size=18),  # Match HR donut
    marker=dict(colors=["#1f77b4", "#aec7e8", "#ff9896"])  # Optional: set consistent colors
)])

donut_fig.update_layout(
    height=550,
    showlegend=True,
    title="AI-Enabled Monthly Cost Breakdown",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(size=16),
    legend=dict(font=dict(size=22)),  # Match other donut
    margin=dict(t=40, b=40, l=60, r=60)
)

st.plotly_chart(donut_fig, use_container_width=True)

# --- 10. Cost Breakdown with Collapsible Details ---
st.markdown("## 🔍 Cost Breakdown Details")
st.markdown(f"""
<details>
  <summary><strong>Human Agent Cost: ${baseline_human_cost:,.0f}</strong></summary>
  <ul>
    <li>Total Monthly Hours: {agent_monthly_hours:.0f}</li>
    <li>Hourly Total: ${(agent_monthly_hours * hourly_cost):,.0f}</li>
    <li>Tax & Benefits: ${(agent_monthly_hours * hourly_cost * (fully_loaded_multiplier - 1)):,.0f}</li>
    <li>Talk Utilization: {(monthly_minutes / (agent_monthly_hours * 60 * agents) * 100):.0f}%</li>
  </ul>
</details>

<details>
  <summary><strong>AI Agent Cost: ${ai_enabled_cost:,.0f}</strong></summary>
  <ul>
    <li>Total Monthly Minutes Automated: {ai_minutes:,.0f}</li>
    <li>AI Usage Cost: ${ai_cost:,.0f}</li>
    <li>Subscription Fee: ${subscription:,.0f}</li>
    <li>Residual Human Cost: ${residual_cost:,.0f}</li>
  </ul>
</details>
""", unsafe_allow_html=True)

# --- 11. FAQ Accordion ---
st.markdown("## ❓ Frequently Asked Questions")
faq = {
    "How does AI reduce payroll costs?": "AI replaces salaries, benefits, and overtime pay associated with human agents.",
    "What kind of cost savings can I expect?": "On average, businesses save up to 50% on communication costs by switching to AI.",
    "Will I save on training expenses?": "AI agents require no onboarding or upskilling, eliminating training budgets.",
    "Can I scale without extra headcount?": "Yes—AI scales on demand with minimal incremental cost."
}
for question, answer in faq.items():
    st.markdown(f"""
<details>
  <summary>{question}</summary>
  <p>{answer}</p>
</details>
""", unsafe_allow_html=True)
