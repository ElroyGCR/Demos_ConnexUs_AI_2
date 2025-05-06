import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from io import BytesIO
import base64

# --- Page & Favicon Setup ---
st.set_page_config("ConnexUS AI ROI Calculator", page_icon="favicon-32x32.png", layout="wide")

def load_base64(path):
    try:
        img = Image.open(path)
        buf = BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    except:
        return None

# Inject favicon
if (f64 := load_base64("favicon-32x32.png")):
    st.markdown(f'<link rel="icon" href="data:image/png;base64,{f64}">', unsafe_allow_html=True)

# --- Transparent Plotly & CSS for Savings Cards ---
TRANSPARENT = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
st.markdown("""
<style>
  /* Remove default padding */
  .block-container { padding-top:0; }
  /* Savings cards layout */
  .savings-cards { display:flex; flex-direction:column; gap:10px; height:100%; }
  .savings-cards .metric-card:last-child { margin-top:auto; }
  /* Make metric cards a uniform size */
  .metric-card { background:#111; border:2px solid #00FFAA; border-radius:12px;
                 padding:15px; width:100%; text-align:center; }
  .metric-label { color:#DDD; font-size:14px; margin-bottom:5px; }
  .metric-value { color:#00FFAA; font-size:32px; font-weight:800; }
</style>
""", unsafe_allow_html=True)

# --- Watermark ---
if (w64 := load_base64("connexus_logo_watermark.png")):
    st.markdown(f"""
    <div style="
      position:fixed; top:80px; left:50%; transform:translateX(-50%);
      width:800px; height:800px; background:url(data:image/png;base64,{w64}) 
      center/contain no-repeat; opacity:0.15; pointer-events:none; z-index:0;
    "></div>
    """, unsafe_allow_html=True)

# --- Title ---
st.markdown("""
# 🚀 ConnexUS AI ROI Calculator
""")

# --- Helper for Metric Cards ---
def metric_block(label, value, prefix="$", suffix=""):
    return f"""
      <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{prefix}{value:,.2f}{suffix}</div>
      </div>
    """

# --- SIDEBAR INPUTS ---
st.sidebar.header("🔧 Inputs")
agents               = st.sidebar.number_input("Agents (FTE)",       min_value=1,    max_value=100, value=25)
human_hourly_rate    = st.sidebar.number_input("Human Hourly Rate ($)", min_value=5.0, max_value=50.0, value=12.0)
burden_pct           = st.sidebar.slider("Burden % (tax+ben.)", 0, 75, 35, step=5) / 100
talk_util_pct        = st.sidebar.slider("Talk Utilization %",  0,100, 40, step=5) / 100
hours_per_month      = st.sidebar.number_input("Hours per Agent (mo)", value=40*4.33)

st.sidebar.markdown("---")
subscription         = st.sidebar.number_input("AI Subscription ($/mo)", value=2000)
integration_fee      = st.sidebar.number_input("One‐time Integration Fee ($)", value=15000)
ai_cost_per_min      = st.sidebar.number_input("AI Cost per Min ($)", value=0.20)
automation_pct       = st.sidebar.slider("Automation % Target", 0,100, 50, step=5) / 100

st.sidebar.markdown("---")
include_indirect     = st.sidebar.checkbox("Include Indirect Value", value=False)
include_hr           = st.sidebar.checkbox("Include HR‐Strategic Value", value=False)
if include_hr:
    hr_pct = st.sidebar.slider("HR Strategic %", 0,50, 10, step=5) / 100
else:
    hr_pct = 0.0

# --- 1) CORE CALCULATIONS ---
# Fully‐loaded multiplier
fl_mult = 1 + burden_pct

# Baseline human cost
agent_monthly_hours = hours_per_month * agents
baseline_human_cost = agent_monthly_hours * human_hourly_rate * fl_mult

# Talkable minutes/mo
talkable_minutes = agent_monthly_hours * talk_util_pct * 60

# AI vs Residual
ai_minutes        = automation_pct * talkable_minutes
residual_minutes  = talkable_minutes - ai_minutes

ai_cost           = ai_minutes * ai_cost_per_min
residual_cost     = (residual_minutes/60) * human_hourly_rate * fl_mult

total_ai_monthly  = ai_cost + residual_cost + subscription

# Direct savings
net_savings       = baseline_human_cost - total_ai_monthly

# Indirect = e.g. time saved × human cost (simplified: same rate)
indirect_savings  = net_savings * automation_pct if include_indirect else 0.0

# HR strategic = e.g. attrition+recruiting savings
strategic_savings = baseline_human_cost * hr_pct if include_hr else 0.0

# $1 → savings on integration+subscription
dollar_return     = (net_savings + indirect_savings + strategic_savings) / (subscription + integration_fee)

# Production‐based ROI & payback
roi_prod_mo       = (net_savings + indirect_savings + strategic_savings) / baseline_human_cost * 100
payback_mo_prod   = baseline_human_cost / (net_savings + indirect_savings + strategic_savings)

# Integration‐based ROI & payback
roi_integ_mo      = (net_savings + indirect_savings + strategic_savings) / integration_fee * 100
roi_integ_yr      = roi_integ_mo * 12
payback_mo_int    = integration_fee / (net_savings + indirect_savings + strategic_savings)
value_basis       = net_savings + indirect_savings + strategic_savings

# --- 2) CORE METRICS ROW ---
st.markdown("---")
st.subheader("📊 Core Financial Metrics")
c1,c2,c3,c4 = st.columns(4, gap="large")
c1.markdown(metric_block("Net Monthly Savings", net_savings), unsafe_allow_html=True)
c2.markdown(metric_block("ROI on Production (mo)", roi_prod_mo, suffix="%"), unsafe_allow_html=True)
c3.markdown(metric_block("Payback on Prod (mo)", payback_mo_prod, suffix=" mo"), unsafe_allow_html=True)
c4.markdown(metric_block("$1 → Savings", dollar_return, prefix="$"), unsafe_allow_html=True)

# --- 3) AI INVESTMENT IMPACT (Large Banner) ---
st.markdown("---")
st.subheader("💡 AI Investment Impact")
st.markdown("<div style='color:#DDD;font-size:14px;margin-bottom:8px;'>"
            "Value returned for every $1 spent on AI usage + subscription.</div>",
            unsafe_allow_html=True)
st.markdown(f"""
<div style='
  background:#111; border:2px solid #00FFAA; border-radius:12px;
  padding:20px; text-align:center;'
>
  <span style='font-size:24px;color:#FFF;'>For every </span>
  <span style='font-size:32px;color:#FFD700;'>$1</span>
  <span style='font-size:24px;color:#FFF;'> you invest in AI, you save: </span>
  <span style='font-size:36px;color:#00FFAA;'>${dollar_return:,.2f}</span>
</div>
""", unsafe_allow_html=True)

# --- 4) HUMAN vs HYBRID COST COMPARISON ---
st.markdown("---")
st.subheader("💰 Human vs Hybrid Cost Comparison")
fig = go.Figure()

# 100% Human
fig.add_trace(go.Bar(
    name="100% Human Cost",
    x=["Scenario"], y=[baseline_human_cost],
    marker_color="#90CAF9"
))
# Hybrid: residual human
fig.add_trace(go.Bar(
    name=f"{int((1-automation_pct)*100)}% Human",
    x=["Scenario"], y=[residual_cost],
    marker_color="#64B5F6"
))
# Hybrid: AI usage + subscription
fig.add_trace(go.Bar(
    name=f"{int(automation_pct*100)}% AI",
    x=["Scenario"], y=[ai_cost + subscription],
    marker_color="#1E88E5"
))

fig.update_layout(
    barmode="stack",
    xaxis=dict(showticklabels=False),
    yaxis_title="Monthly Spend ($)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    margin=dict(t=40,b=20,l=0,r=0),
    **TRANSPARENT
)
st.plotly_chart(fig, use_container_width=True)

# --- 5) SAVINGS BREAKDOWN + METRIC CARDS ---
st.markdown("---")
st.subheader("💸 Savings Breakdown")
left, right = st.columns([3,1], gap="large")

with left:
    fig_sav = go.Figure()
    # Net Savings
    fig_sav.add_trace(go.Bar(
        name="Net Savings", x=["Savings"], y=[net_savings],
        marker_color="#66BB6A"
    ))
    # Indirect
    if include_indirect:
        fig_sav.add_trace(go.Bar(
            name="Indirect Sav.", x=["Savings"], y=[indirect_savings],
            marker_color="#FFA726"
        ))
    # HR strategic
    if include_hr:
        fig_sav.add_trace(go.Bar(
            name="HR Strategic", x=["Savings"], y=[strategic_savings],
            marker_color="#29B6F6"
        ))

    fig_sav.update_layout(
        barmode="stack",
        xaxis=dict(showticklabels=False),
        yaxis_title="Monthly Savings ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=40,b=20,l=0,r=0),
        **TRANSPARENT
    )
    st.plotly_chart(fig_sav, use_container_width=True)

with right:
    st.markdown("<div class='savings-cards'>", unsafe_allow_html=True)
    st.markdown(metric_block("Net Savings", net_savings), unsafe_allow_html=True)
    if include_indirect:
        st.markdown(metric_block("Indirect Sav.", indirect_savings), unsafe_allow_html=True)
    if include_hr:
        st.markdown(metric_block("HR Strategic", strategic_savings), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 6) INTEGRATION METRICS ---
st.markdown("---")
st.subheader("💼 Integration Basis Metrics")
i1,i2,i3,i4 = st.columns(4, gap="large")
i1.markdown(metric_block("ROI on Integration (mo)", roi_integ_mo, suffix="%"), unsafe_allow_html=True)
i2.markdown(metric_block("ROI on Integration (yr)", roi_integ_yr, suffix="%"), unsafe_allow_html=True)
i3.markdown(metric_block("Payback on Int (mo)", payback_mo_int, suffix=" mo"), unsafe_allow_html=True)
i4.markdown(metric_block("Value Basis", value_basis), unsafe_allow_html=True)
