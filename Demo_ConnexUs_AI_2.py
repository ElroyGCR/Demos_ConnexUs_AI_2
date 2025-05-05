import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import plotly.graph_objects as go

# --- Page Setup ---
st.set_page_config(page_title="ConnexUS AI ROI Calculator",
                   page_icon="favicon-32x32.png",
                   layout="wide")

# --- Favicon Injection ---
def load_favicon_base64(path="favicon-32x32.png"):
    try:
        img = Image.open(path)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")
    except:
        return None

favicon_b64 = load_favicon_base64()
if favicon_b64:
    st.markdown(f"""
        <link rel="icon" type="image/png" sizes="32x32"
              href="data:image/png;base64,{favicon_b64}">
    """, unsafe_allow_html=True)

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
    st.markdown(f"""
        <style>
        .watermark {{
            position: fixed;
            top: 80px;
            left: 50%;
            transform: translateX(-50%);
            width: 800px;
            height: 800px;
            opacity: 0.15;
            pointer-events: none;
            background: url("data:image/png;base64,{watermark_b64}") no-repeat
                        center center / contain;
            z-index: 0;
        }}
        </style>
        <div class="watermark"></div>
    """, unsafe_allow_html=True)

# --- Styles & Utilities ---
TRANSPARENT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
)

def metric_block(label, value, icon=None, color="#00FFAA", border="#00FFAA",
                 prefix="", suffix=""):
    icon_html = (f"<img src='{icon}' width='16' "
                 "style='vertical-align:middle; margin-right:6px;'/>") if icon else ""
    return f"""
    <div style='
        display:inline-block;
        background-color: rgba(17,17,17,0.8);
        border: 2px solid {border};
        border-radius: 12px;
        padding: 12px 20px;
        margin: 5px;
        z-index:1;
    '>
      <div style='color:#EEE; font-size:14px; margin-bottom:4px;'>
        {icon_html}{label}
      </div>
      <div style='color:{color}; font-size:32px; font-weight:600;'>
        {prefix}{value:,.1f}{suffix}
      </div>
    </div>
    """

def small_metric_card(label, value, prefix="", suffix=""):
    return f"""
    <div style='
        display:inline-block;
        background-color: rgba(17,17,17,0.8);
        border: 1px solid #00FFAA;
        border-radius: 8px;
        padding: 8px 12px;
        margin: 3px;
        text-align:center;
        z-index:1;
    '>
      <div style='color:#AAA; font-size:11px; margin-bottom:3px;'>{label}</div>
      <div style='color:#00FFAA; font-size:18px; font-weight:600;'>
        {prefix}{value:,.1f}{suffix}
      </div>
    </div>
    """

def caption(text):
    return f"<div style='color:#DDD; font-size:14px; margin-bottom:8px;'>{text}</div>"

# --- Title ---
st.markdown("""
    <h1 style='color:white; font-size:2.4rem; font-weight:800;
               margin-bottom:0.2rem; z-index:1;'>
      ConnexUS AI ROI Calculator
    </h1>
    <hr style='border-top:1px solid #333; margin-bottom:1rem;'>
""", unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
st.sidebar.header("📊 Input Your Call Center Data")

# Revenue & Volume
st.sidebar.subheader("📈 Revenue & Volume")
monthly_revenue    = st.sidebar.number_input("Monthly Revenue ($)", value=250_000, step=10_000)
weekly_interactions= st.sidebar.number_input("Weekly Interactions", value=10_000, step=100)
aht                = st.sidebar.slider("Average Handle Time (minutes)", 1, 20, 6)

# Workforce & Agent Metrics
st.sidebar.subheader("👥 Workforce & Agent Metrics")
agents             = st.sidebar.number_input("Agents (FTE)", value=25, min_value=1)
hourly_cost        = st.sidebar.number_input("Agent Hourly Cost ($)", value=12.0, min_value=5.0, max_value=50.0)
burden_pct         = st.sidebar.slider("Burden % (Taxes & Benefits)", 0, 75, 35, step=5)
talk_pct           = st.sidebar.slider("Talk Utilization %", 0, 100, 40, step=5)
hours_per_month    = st.sidebar.number_input("Hours per Agent / Month", value=40*4.33)

# Business Impact Assumptions
st.sidebar.subheader("💼 Business Impact Assumptions")
production_pct     = st.sidebar.number_input("Production Improvement (%)", value=25.0, step=0.1)
upsell_pct         = st.sidebar.number_input("Upsell Improvement (%)",    value=10.0, step=0.1)

# AI Cost Inputs
st.sidebar.subheader("🤖 AI Cost Inputs")
subscription       = st.sidebar.number_input("AI Subscription ($/mo)", value=2_000, step=100)
integration_fee    = st.sidebar.number_input("Integration Fee ($)",     value=15_000, step=500)
ai_cost_per_min    = st.sidebar.number_input("AI Cost per Minute ($)", value=0.20, step=0.01)
automation_pct     = st.sidebar.slider("Automation % Target", 0, 100, 50, step=5)

# ROI Toggles
st.sidebar.subheader("⚙️ ROI Options")
use_indirects      = st.sidebar.checkbox("Include Indirect Value", value=True)
include_strategic  = st.sidebar.checkbox("Include Strategic HR Savings", value=False)
strategic_pct      = st.sidebar.slider("Strategic HR Savings (%)",
                                       0, 50, 25, step=5) if include_strategic else 0

# --- CALCULATIONS ---

# 1. Total Monthly Workload
monthly_minutes    = weekly_interactions * aht * 4.33

# 2. AI vs Residual Human Cost
ai_minutes         = (automation_pct/100) * monthly_minutes
residual_minutes   = monthly_minutes - ai_minutes

ai_cost            = ai_minutes * ai_cost_per_min
fully_loaded_mul   = 1 + (burden_pct/100)
residual_cost      = (residual_minutes/60) * hourly_cost * fully_loaded_mul

subscription_cost  = subscription
total_ai_spend     = ai_cost + subscription_cost
ai_enabled_cost    = ai_cost + residual_cost + subscription_cost

# 3. Indirect Savings (Production & Upsell)
production_savings = (monthly_minutes*(production_pct/100)/60) \
                     * hourly_cost * fully_loaded_mul
upsell_savings     = monthly_revenue * (upsell_pct/100)
indirect_savings   = production_savings + upsell_savings

# 4. Baseline Human Cost
agent_monthly_hours= hours_per_month
minutes_per_agent  = agent_monthly_hours * 60
required_agents    = monthly_minutes / minutes_per_agent
effective_agents   = max(agents, required_agents)

baseline_human_cost= (
    effective_agents
  * agent_monthly_hours
  * hourly_cost
  * fully_loaded_mul
)

# 5. Net Direct Savings
net_savings        = baseline_human_cost - ai_enabled_cost

# 6. Strategic HR Savings
strategic_savings  = net_savings * (strategic_pct/100)

# 7. Total Value Basis
value_basis        = net_savings
if use_indirects:
    value_basis   += indirect_savings
if include_strategic:
    value_basis   += strategic_savings

# 8. ROI & Payback (Operating)
roi_monthly        = (value_basis / ai_enabled_cost) * 100 if ai_enabled_cost else 0
annual_roi         = roi_monthly * 12
payback_days       = (integration_fee / value_basis) * 30 if value_basis else float('inf')

# 9. ROI & Payback (Integration)
integration_roi    = (value_basis / integration_fee) * 100 if integration_fee else 0
integration_payback= integration_fee / value_basis if value_basis else float('inf')

# 10. Cost Efficiency & Savings per Dollar
cost_efficiency    = ((baseline_human_cost - ai_enabled_cost)
                     / baseline_human_cost) * 100 if baseline_human_cost else 0
dollar_saved_per_dollar = (value_basis / total_ai_spend
                           if total_ai_spend else 0)

# --- UI OUTPUTS ---

st.markdown("## 📊 Core Financial Metrics (Operating Basis)")
st.markdown(caption("These values reflect cost savings vs. a fully human‐run operation."))
c1,c2,c3,c4 = st.columns(4)
with c1:
    st.markdown(metric_block("Net Savings",       net_savings,
                             icon="favicon-16x16.png", prefix="$"), unsafe_allow_html=True)
with c2:
    st.markdown(metric_block("Cost Eff.",         cost_efficiency,
                             icon="favicon-16x16.png", suffix="%"), unsafe_allow_html=True)
with c3:
    st.markdown(metric_block("ROI (Mo)",          roi_monthly,
                             icon="favicon-16x16.png", suffix="%"), unsafe_allow_html=True)
with c4:
    st.markdown(metric_block("Payback (mo)",      integration_payback,
                             icon="favicon-16x16.png", suffix=" mo"), unsafe_allow_html=True)

st.markdown("---")
st.markdown("## 🚀 AI Investment Impact")
st.markdown(caption("Value returned for every \$1 spent on AI usage + subscription."))
st.markdown(
    metric_block("$1 spent →", dollar_saved_per_dollar,
                 icon="favicon-32x32.png", prefix="$"),
    unsafe_allow_html=True
)

st.markdown("---")
st.markdown("## 💼 Key Metrics (Integration Basis)")
st.markdown(caption("Returns compared to your one-time integration fee."))
i1,i2,i3,i4 = st.columns(4)
with i1:
    st.markdown(metric_block("ROI (Mo)",   integration_roi,
                             icon="favicon-16x16.png", suffix="%"), unsafe_allow_html=True)
with i2:
    st.markdown(metric_block("Annual ROI", integration_roi*12,
                             icon="favicon-16x16.png", suffix="%"), unsafe_allow_html=True)
with i3:
    st.markdown(metric_block("Payback",    integration_payback,
                             icon="favicon-16x16.png", suffix=" mo"), unsafe_allow_html=True)
with i4:
    st.markdown(metric_block("Total Value", value_basis,
                             icon="favicon-16x16.png", prefix="$"), unsafe_allow_html=True)

st.markdown("---")
st.markdown("## 🍩 AI Cost Composition")
st.markdown(caption("AI usage vs. residual labor vs. subscription"))
pie = go.Figure(data=[go.Pie(
    labels=["AI Usage","Residual Labor","Subscription"],
    values=[ai_cost, residual_cost, subscription_cost],
    hole=0.5,textinfo="label+percent",
)])
pie.update_layout(**TRANSPARENT_LAYOUT, showlegend=True)
st.plotly_chart(pie, use_container_width=True)

# --- Savings Over Time Plot ---
def plot_savings_over_time(net, net_ind=None, all_val=None):
    months = [1,6,12,18,24,36,48,60]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        name="Net Saving", x=months,
        y=[net*m for m in months],
        mode="lines+markers"
    ))
    if net_ind is not None:
        fig.add_trace(go.Scatter(
            name="Net+Indirect", x=months,
            y=[(net+indirect_savings)*m for m in months],
            mode="lines+markers"
        ))
    if all_val is not None:
        fig.add_trace(go.Scatter(
            name="All Savings", x=months,
            y=[all_val*m for m in months],
            mode="lines+markers"
        ))
    fig.update_layout(
        title="Cumulative Savings Over Time",
        xaxis_title="Months", yaxis_title="Savings ($)",
        **TRANSPARENT_LAYOUT
    )
    st.plotly_chart(fig, use_container_width=True)

plot_savings_over_time(
    net_savings,
    net_savings+indirect_savings if use_indirects else None,
    value_basis if include_strategic else None
)
