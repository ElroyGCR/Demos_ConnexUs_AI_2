import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from io import BytesIO
import base64

# ─── Page & Favicon Setup ──────────────────────────────────────────────
st.set_page_config(page_title="ConnexUS AI ROI Calculator", layout="wide")

def load_base64(path):
    try:
        img = Image.open(path)
        buf = BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    except:
        return None

favicon_b64 = load_base64("favicon-32x32.png")
if favicon_b64:
    st.markdown(
        f"""<link rel="icon" href="data:image/png;base64,{favicon_b64}" type="image/png">""",
        unsafe_allow_html=True,
    )

# ─── Global Styles & Watermark ────────────────────────────────────────
st.markdown("""
    <style>
      .block-container { padding-top: 1rem !important; }
      .metric-card { background-color: rgba(0,0,0,0.5); border: 2px solid #00FFAA;
                     border-radius: 12px; padding: 15px; text-align:center; }
      .metric-label { color: #DDD; font-size:14px; }
      .metric-value { color: #00FFAA; font-size: 32px; font-weight:bold; }
    </style>
""", unsafe_allow_html=True)

wm = load_base64("connexus_logo_watermark.png")
if wm:
    st.markdown(f"""
      <div style="
        position:fixed; top:50px; right:10%;
        width:400px; height:400px; opacity:0.1;
        background:url(data:image/png;base64,{wm}) no-repeat center/contain;
        pointer-events:none;
      "></div>
    """, unsafe_allow_html=True)

# ─── Helper Functions ──────────────────────────────────────────────────
def metric_block(label, value, prefix="$", suffix=""):
    return f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{prefix}{value:,.2f}{suffix}</div>
    </div>
    """

TRANSPARENT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# ─── Sidebar Inputs ───────────────────────────────────────────────────
st.sidebar.header("⚙️ Inputs")

# Workforce & Agent Metrics
agents          = st.sidebar.number_input("Agents (FTE)", min_value=1, value=25, step=1)
human_rate      = st.sidebar.number_input("Human Hourly Cost ($)", min_value=5.0, value=12.0, step=1.0)
burden_pct      = st.sidebar.slider("Burden (Benefits %)​", 0, 75, 35, step=5)
talk_pct        = st.sidebar.slider("Talk Utilization (%)", 0, 100, 40, step=5)
hours_per_month = st.sidebar.number_input("Hours per Agent / Month", value=173.2, step=1.0)

# AI Cost Inputs
st.sidebar.subheader("🤖 AI Cost Inputs")
subscription    = st.sidebar.number_input("AI Subscription ($/mo)", value=2000, step=100)
integration_fee = st.sidebar.number_input("Integration Fee ($)", value=15000, step=500)
ai_cost_min     = st.sidebar.number_input("AI Cost per Min ($)", value=0.20, step=0.01)
automation_pct  = st.sidebar.slider("Automation Target (%)", 0, 100, 50, step=5)

# Indirect & HR Strategic Toggles
st.sidebar.subheader("📈 Value Adders")
include_indirect = st.sidebar.checkbox("Include Indirect Value", value=True)
production_pct    = st.sidebar.slider("Production Improvement (%)", 0, 100, 25, step=5)
include_hr        = st.sidebar.checkbox("Include HR Strategic Impact", value=False)
if include_hr:
    hr_pct = st.sidebar.slider("HR Impact (%)", 0, 50, 10, step=5)
else:
    hr_pct = 0

# ─── Core Calculations ─────────────────────────────────────────────────
# Burden multiplier
burden_mul = 1 + burden_pct/100

# Baseline human cost
baseline_human_cost = agents * hours_per_month * human_rate * burden_mul

# Monthly talk minutes (only the utilized portion)
monthly_talk_mins = agents * hours_per_month * (talk_pct/100) * 60

# AI usage cost
ai_mins      = (automation_pct/100) * monthly_talk_mins
ai_usage_cost = ai_mins * ai_cost_min

# Residual human cost (the portion you didn't automate)
residual_human_hours = agents * hours_per_month * (1 - automation_pct/100)
residual_cost         = residual_human_hours * human_rate * burden_mul

# Total AI-enabled monthly cost
ai_enabled_cost = ai_usage_cost + residual_cost + subscription

# Net direct savings
net_savings = baseline_human_cost - ai_enabled_cost

# Indirect savings (production uplift on full baseline)
indirect_savings = baseline_human_cost * (production_pct/100) if include_indirect else 0

# HR strategic savings (as a % of indirect)
strategic_savings = indirect_savings * (hr_pct/100) if include_hr else 0

# Value basis for ROI & payback
value_basis = net_savings + indirect_savings + strategic_savings

# ROI & Payback on Integration
roi_integ_mo      = (value_basis / integration_fee) * 100 if integration_fee>0 else 0
roi_integ_yr      = roi_integ_mo * 12
payback_mo_integ  = integration_fee / value_basis if value_basis>0 else float('inf')

# ROI & Payback on Production basis
roi_prod_mo       = (value_basis / baseline_human_cost) * 100 if baseline_human_cost>0 else 0
payback_mo_prod   = baseline_human_cost / value_basis if value_basis>0 else float('inf')

# $1 spent on AI
dollar_return     = (value_basis / (subscription + ai_usage_cost)) if (subscription+ai_usage_cost)>0 else 0

# ─── Main Layout ───────────────────────────────────────────────────────
st.title("🚀 ConnexUS AI ROI Calculator")
st.markdown("---")

# Core Metrics Row
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(metric_block("Net Monthly Savings", net_savings), unsafe_allow_html=True)
with c2:
    st.markdown(metric_block("ROI on Production (mo)", roi_prod_mo, suffix="%"), unsafe_allow_html=True)
with c3:
    st.markdown(metric_block("Payback on Prod (mo)", payback_mo_prod, suffix=" mo"), unsafe_allow_html=True)
with c4:
    st.markdown(metric_block("$1 → Savings", dollar_return, prefix="$"), unsafe_allow_html=True)

st.markdown("---")

# Integration Metrics Row
i1, i2, i3, i4 = st.columns(4)
with i1:
    st.markdown(metric_block("ROI on Integration (mo)", roi_integ_mo, suffix="%"), unsafe_allow_html=True)
with i2:
    st.markdown(metric_block("ROI on Integration (yr)", roi_integ_yr, suffix="%"), unsafe_allow_html=True)
with i3:
    st.markdown(metric_block("Payback on Int (mo)", payback_mo_integ, suffix=" mo"), unsafe_allow_html=True)
with i4:
    st.markdown(metric_block("Value Basis", value_basis), unsafe_allow_html=True)

st.markdown("---")

# ─── AI Investment Impact ─────────────────────────────────────────────
st.markdown("## 💡 AI Investment Impact", unsafe_allow_html=True)

st.markdown("""
    <p style='text-align:center; font-size:16px; color:#aaa;'>
    Shows how much value is returned for every dollar spent on AI — includes cost savings and indirect gains.
    </p>
""", unsafe_allow_html=True)

ai_spend = subscription + ai_usage_cost
base_return = net_savings / ai_spend if ai_spend else 0.0

extra = 0.0
if include_indirect:
    extra += indirect_savings / ai_spend
if include_hr:
    extra += strategic_savings / ai_spend

dollar_return = base_return + extra

st.markdown(f"""
<div style='
    background-color: rgba(0,0,0,0.25);
    border: 2px solid #00FFAA;
    border-radius: 12px;
    padding: 20px 30px;
    margin-top: 10px;
    margin-bottom: 20px;
    color: white;
    font-size: 30px;
    font-weight: 500;
    text-align: center;
'>
    For every <span style="color:#FFD700; font-size:46px; font-weight:800;">$1</span> you invest in AI, you save:
    <span style="color:#00FFAA; font-size:50px; font-weight:900;">${dollar_return:,.2f}</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─── Human vs Hybrid Cost Comparison ───────────────────────────────
st.subheader("💰 Human vs Hybrid Cost Comparison")
fig1 = go.Figure()
cats = ["100% Human", "Hybrid"]

# 100% Human bar
fig1.add_trace(go.Bar(
    name="100% Human Cost",
    x=cats, y=[baseline_human_cost, 0],
    marker_color="#90CAF9",
))
# Residual Human (Hybrid)
fig1.add_trace(go.Bar(
    name=f"{100-automation_pct}% Human",
    x=cats, y=[0, residual_cost],
    marker_color="#64B5F6",
))
# AI Usage
fig1.add_trace(go.Bar(
    name=f"{automation_pct}% AI Usage",
    x=cats, y=[0, ai_usage_cost],
    marker_color="#1E88E5",
))
# Subscription
fig1.add_trace(go.Bar(
    name="Subscription",
    x=cats, y=[0, subscription],
    marker_color="#FFAB91",
))

fig1.update_layout(
    barmode="stack",
    xaxis_title="",
    yaxis_title="Monthly Spend ($)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(t=30, b=30, l=0, r=0),
    **TRANSPARENT_LAYOUT
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ─── Savings Breakdown ───────────────────────────────────────────────
st.subheader("💸 Savings Breakdown")
left, right = st.columns([3,1], gap="large")

# — left side stays as is —
with left:
    fig2 = go.Figure()
    # Net
    fig2.add_trace(go.Bar(
        name="Net Savings",
        x=["Savings"], y=[net_savings],
        marker_color="#66BB6A"
    ))
    # Indirect
    if include_indirect:
        fig2.add_trace(go.Bar(
            name="Indirect Sav.",
            x=["Savings"], y=[indirect_savings],
            marker_color="#FFA726"
        ))
    # HR Strategic
    if include_hr:
        fig2.add_trace(go.Bar(
            name="HR Strategic",
            x=["Savings"], y=[strategic_savings],
            marker_color="#29B6F6"
        ))
    fig2.update_layout(
        barmode='stack',
        xaxis=dict(showticklabels=False),
        yaxis_title="Monthly Savings ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=30, b=30, l=0, r=0),
        **TRANSPARENT_LAYOUT
    )
    st.plotly_chart(fig2, use_container_width=True)

# — right side: three cards, 10px gap, pushed down to match chart height —
with right:
    html = f"""
    <div style='
        display: flex;
        flex-direction: column;
        row-gap: 10px;
        margin-top: 60px;
    '>
      {metric_block("Net Savings",      net_savings)}
      {metric_block("Indirect Sav.",    indirect_savings) if include_indirect else ""}
      {metric_block("HR Strategic",     strategic_savings) if include_hr     else ""}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
