import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from io import BytesIO
import base64
from decimal import Decimal, ROUND_HALF_UP

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
    st.markdown(f"""<link rel="icon" href="data:image/png;base64,{favicon_b64}" type="image/png">""", unsafe_allow_html=True)

watermark_b64 = load_base64("connexus_logo_watermark.png")
if watermark_b64:
    st.markdown(f"""
    <style>
    .watermark {{
      position:fixed; top:10px; left:55%;
      transform:translateX(-50%);
      width:800px; height:800px;
      opacity:0.12; z-index:0;
      background:url("data:image/png;base64,{watermark_b64}") 
                 no-repeat center/contain;
      pointer-events:none;
    }}
    </style>
    <div class="watermark"></div>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
  .block-container { padding-top: 1rem !important; }
  .metric-card { background-color: rgba(0,0,0,0.25); border: 2px solid #00FFAA; border-radius: 12px; padding: 15px; text-align:center; }
  .metric-label { color: #DDD; font-size:14px; }
  .metric-value { color: #00FFAA; font-size: 32px; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

def metric_block(label, value, prefix="", suffix="", value_format="{:,.2f}"):
    if value == float('inf') or value != value:
        formatted_value = "N/A"
        prefix = ""
        suffix = ""
    else:
        formatted_value = value_format.format(value)
    return f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{prefix}{formatted_value}{suffix}</div>
    </div>
    """

def excel_round(val, decimals=1):
    if val == float('inf') or val != val:
        return float('inf')
    return float(Decimal(val).quantize(Decimal('1.' + '0'*decimals), rounding=ROUND_HALF_UP))

TRANSPARENT_LAYOUT = dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

# Sidebar Inputs
st.sidebar.header("⚙️ Inputs")
agents = st.sidebar.number_input("Agents (FTE)", min_value=1, value=15, step=1)
human_rate = st.sidebar.number_input("Human Hourly Cost ($)", min_value=5.0, value=12.0, step=1.0)
burden_pct = st.sidebar.slider("Burden (Benefits %)", 0, 75, 35, step=5)
talk_pct = st.sidebar.slider("Talk Utilization (%)", 0, 100, 40, step=5)
hours_per_month = st.sidebar.number_input("Hours per Agent / Month", value=173.2, step=1.0)

st.sidebar.subheader("🤖 AI Cost Inputs")
subscription = st.sidebar.number_input("AI Subscription ($/mo)", value=2000, step=100)
integration_fee = st.sidebar.number_input("Integration Fee ($)", value=15000, step=500)
ai_cost_min = st.sidebar.number_input("AI Cost per Min ($)", value=0.20, step=0.01)
automation_pct = st.sidebar.slider("Automation Target (%)", 0, 100, 50, step=5)

st.sidebar.subheader("📈 Value Adders")
include_indirect = st.sidebar.checkbox("Include Indirect Value", value=True)
production_pct = st.sidebar.slider("Production Improvement (%)", 0, 100, 25, step=5)
include_hr = st.sidebar.checkbox("Include HR Strategic Impact", value=False)
hr_pct = st.sidebar.slider("HR Impact (%)", 0, 50, 10, step=5) if include_hr else 0

# Core Calculations
burden_mul = 1 + burden_pct/100
baseline_human_cost = agents * hours_per_month * human_rate * burden_mul
monthly_total_mins = agents * hours_per_month * 60
ai_mins = (automation_pct/100) * monthly_total_mins
ai_usage_cost = ai_mins * ai_cost_min
residual_human_hours = agents * hours_per_month * (1 - automation_pct/100)
residual_cost = residual_human_hours * human_rate * burden_mul
ai_enabled_cost = ai_usage_cost + residual_cost + subscription
net_savings = baseline_human_cost - ai_enabled_cost

indirect_savings = baseline_human_cost * (production_pct/100) if include_indirect else 0
strategic_savings = indirect_savings * (hr_pct/100) if include_hr else 0
value_basis = net_savings + indirect_savings + strategic_savings

monthly_cost_efficiency = (value_basis / baseline_human_cost) * 100 if baseline_human_cost > 0 else float('inf')
roi_prod_mo = (value_basis / baseline_human_cost) * 100 if baseline_human_cost > 0 else 0
payback_mo_prod = baseline_human_cost / value_basis if value_basis > 0 else float('inf')

roi_integ_mo = (value_basis / integration_fee) * 100 if integration_fee > 0 else 0
roi_integ_yr = roi_integ_mo * 12
payback_mo_integ = integration_fee / value_basis if value_basis > 0 else float('inf')

ai_spend = subscription + ai_usage_cost
if ai_spend > 0:
    dollar_return = value_basis / ai_spend
else:
    dollar_return = 0

# Main Layout
st.title("🚀 ConnexUS AI ROI Calculator")
st.markdown("---")

# Core Metrics
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(metric_block("Net Monthly Savings", net_savings, "$", "", "{:,.0f}"), unsafe_allow_html=True)
with c2:
    st.markdown(metric_block("ROI on Production (mo)", roi_prod_mo, "", "%", "{:,.1f}"), unsafe_allow_html=True)
with c3:
    st.markdown(metric_block("Payback on Prod (mo)", payback_mo_prod, "", " mo", "{:,.2f}"), unsafe_allow_html=True)
with c4:
    st.markdown(metric_block("Monthly Cost Efficiency", monthly_cost_efficiency, "", "%", "{:,.1f}"), unsafe_allow_html=True)

# Integration Metrics
i1, i2, i3, i4 = st.columns(4)
with i1:
    st.markdown(metric_block("ROI on Integration (mo)", roi_integ_mo, "", "%", "{:,.1f}"), unsafe_allow_html=True)
with i2:
    st.markdown(metric_block("ROI on Integration (yr)", roi_integ_yr, "", "%", "{:,.1f}"), unsafe_allow_html=True)
with i3:
    st.markdown(metric_block("Payback on Int (mo)", payback_mo_integ, "", " mo", "{:,.2f}"), unsafe_allow_html=True)
with i4:
    st.markdown(metric_block("Value Basis", value_basis, "$", "", "{:,.0f}"), unsafe_allow_html=True)

st.markdown("---")

# AI Investment Impact
st.markdown("## 💡 AI Investment Impact", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center; font-size:16px; color:#aaa;'>
Shows how much value is returned for every dollar spent on AI — includes cost savings, indirect and strategic gains.
</p>
""", unsafe_allow_html=True)

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

# Human vs Hybrid Cost Comparison
st.subheader("💰 Human vs Hybrid Cost Comparison")
fig1 = go.Figure()
cats = ["100% Human", "Hybrid"]

fig1.add_trace(go.Bar(name="100% Human Cost", x=cats, y=[baseline_human_cost, 0], marker_color="#90CAF9"))
fig1.add_trace(go.Bar(name=f"{100-automation_pct}% Human", x=cats, y=[0, residual_cost], marker_color="#64B5F6"))
fig1.add_trace(go.Bar(name=f"{automation_pct}% AI Usage", x=cats, y=[0, ai_usage_cost], marker_color="#1E88E5"))
fig1.add_trace(go.Bar(name="Subscription", x=cats, y=[0, subscription], marker_color="#FFAB91"))

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

# Savings Breakdown
st.subheader("💸 Savings Breakdown")
left, right = st.columns([3, 1], gap="large")

with left:
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name="Net Savings", x=["Savings"], y=[net_savings], marker_color="#66BB6A"))
    if include_indirect:
        fig2.add_trace(go.Bar(name="Indirect Savings", x=["Savings"], y=[indirect_savings], marker_color="#FFA726"))
    if include_hr:
        fig2.add_trace(go.Bar(name="HR Strategic", x=["Savings"], y=[strategic_savings], marker_color="#29B6F6"))

    fig2.update_layout(
        barmode='stack',
        xaxis=dict(showticklabels=False),
        yaxis_title="Monthly Savings ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=30, b=30, l=0, r=0),
        **TRANSPARENT_LAYOUT
    )

    st.plotly_chart(fig2, use_container_width=True)

with right:
    html = f"""
    <div style='
        display: flex;
        flex-direction: column;
        row-gap: 10px;
        margin-top: 60px;
    '>
      {metric_block("Net Savings", net_savings, "$", "", "{:,.0f}")}
      {metric_block("Indirect Savings", indirect_savings, "$", "", "{:,.0f}") if include_indirect else ""}
      {metric_block("HR Strategic", strategic_savings, "$", "", "{:,.0f}") if include_hr else ""}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
