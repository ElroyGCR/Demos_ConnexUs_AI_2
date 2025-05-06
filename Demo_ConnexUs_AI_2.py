import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from io import BytesIO
import base64

# --- Page Setup & Favicon ---
st.set_page_config(page_title="ConnexUS AI ROI Calculator",
                   page_icon="favicon-32x32.png", layout="wide")

def load_base64(path):
    try:
        img = Image.open(path)
        buf = BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    except:
        return None

if (f64 := load_base64("favicon-32x32.png")):
    st.markdown(f'<link rel="icon" href="data:image/png;base64,{f64}">',
                unsafe_allow_html=True)

# --- CSS & Watermark ---
st.markdown("""
<style>
  .block-container { padding-top: 0; }
  .metric-card {
    background: #111; border: 2px solid #00FFAA; border-radius:12px;
    padding:15px; width:100%; text-align:center; margin-bottom:10px;
  }
  .metric-label { color:#DDD; font-size:14px; margin-bottom:5px; }
  .metric-value { color:#00FFAA; font-size:32px; font-weight:800; }
  .savings-cards { display:flex; flex-direction:column; gap:10px; height:100%; }
  .savings-cards .metric-card:last-child { margin-top:auto; }
</style>
""", unsafe_allow_html=True)

if (w64 := load_base64("connexus_logo_watermark.png")):
    st.markdown(f"""
    <div style="
      position:fixed; top:80px; left:50%; transform:translateX(-50%);
      width:900px; height:900px; background:
      url(data:image/png;base64,{w64}) center/contain no-repeat;
      opacity:0.15; pointer-events:none; z-index:0;
    "></div>
    """, unsafe_allow_html=True)

TRANSPARENT = dict(paper_bgcolor="rgba(0,0,0,0)",
                   plot_bgcolor="rgba(0,0,0,0)")

# --- Header ---
st.markdown("# 🚀 ConnexUS AI ROI Calculator")

# --- Helper to render a little card ---
def card(label, val):
    return f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{val}</div>
    </div>
    """

# --- Sidebar Inputs ---
st.sidebar.header("🔧 Inputs")
agents         = st.sidebar.number_input("Agents (FTE)", 1, 100, 25)
hourly_rate    = st.sidebar.number_input("Human Hourly Rate ($)", 5.0, 50.0, 12.0)
burden_pct     = st.sidebar.slider("Burden %", 0, 75, 35, 5) / 100
util_pct       = st.sidebar.slider("Talk Utilization %", 0, 100, 40, 5) / 100
hrs_per_month  = st.sidebar.number_input("Hours per Agent (mo)", 40 * 4.33)

st.sidebar.markdown("---")
subscription   = st.sidebar.number_input("AI Subscription ($/mo)", 0, 10000, 2000)
integration    = st.sidebar.number_input("Integration Fee ($)", 0, 100000, 15000)
ai_cost_min    = st.sidebar.number_input("AI Cost per Min ($)", 0.01, 5.0, 0.20)
automation_pct = st.sidebar.slider("Automation %", 0, 100, 50, 5) / 100

st.sidebar.markdown("---")
include_indirect = st.sidebar.checkbox("Include Indirect Value", False)
include_hr       = st.sidebar.checkbox("Include HR-Strategic Value", False)
hr_pct = 0.0
if include_hr:
    hr_pct = st.sidebar.slider("HR Strategic %", 0, 50, 10, 5) / 100

# --- Core Calculations ---
fl_mult = 1 + burden_pct
total_human_hrs = hrs_per_month * agents
baseline_human  = total_human_hrs * hourly_rate * fl_mult

talkable_minutes = total_human_hrs * 60 * util_pct
ai_minutes       = automation_pct * talkable_minutes
res_minutes      = talkable_minutes - ai_minutes

ai_cost          = ai_minutes * ai_cost_min
res_cost         = (res_minutes / 60) * hourly_rate * fl_mult
total_ai_cost    = ai_cost + res_cost + subscription

net_savings      = baseline_human - total_ai_cost
indirect_savings = net_savings * automation_pct if include_indirect else 0
hr_savings       = baseline_human * hr_pct       if include_hr       else 0

value_prod       = net_savings + indirect_savings + hr_savings

# $1 → savings (whole dollars)
dollar_return = int(value_prod / (subscription + integration or 1))

# Prod ROI/payback
roi_prod = (value_prod / baseline_human * 100) if baseline_human else 0
payback_prod = (baseline_human / value_prod) if value_prod else float('inf')

# Integration ROI/payback
roi_int_mo = (value_prod / integration * 100) if integration else 0
roi_int_yr = roi_int_mo * 12
payback_int = (integration / value_prod) if value_prod else float('inf')

# --- 1) Core Financial Metrics ---
st.markdown("---")
st.subheader("📊 Core Financial Metrics")
c1,c2,c3,c4 = st.columns(4, gap="large")
c1.markdown(card("Net Monthly Savings",    f"${net_savings:,.0f}"),  unsafe_allow_html=True)
c2.markdown(card("ROI on Production (mo)", f"{roi_prod:.1f}%"),    unsafe_allow_html=True)
c3.markdown(card("Payback on Prod (mo)",   f"{payback_prod:.1f} mo"),unsafe_allow_html=True)
c4.markdown(card("$1 → Savings",           f"${dollar_return}"),   unsafe_allow_html=True)

# --- 2) AI Investment Impact ---
st.markdown("---")
st.subheader("💡 AI Investment Impact")
st.markdown(
    "<div style='color:#DDD;font-size:14px;margin-bottom:8px;'>"
    "Value returned for every $1 spent on AI usage + subscription.</div>",
    unsafe_allow_html=True
)
st.markdown(f"""
<div class="metric-card" style="border-color:#FFD700;">
  <div class="metric-label">
    For every <span style="color:#FFD700;font-size:24px;">$1</span> you invest in AI, you save:
  </div>
  <div class="metric-value">${dollar_return}</div>
</div>
""", unsafe_allow_html=True)

# --- 3) Human vs Hybrid Cost Comparison ---
st.markdown("---")
st.subheader("💰 Human vs Hybrid Cost Comparison")

# Define categories
categories = ["100% Human", "Hybrid"]

fig = go.Figure()

# 1) 100% Human bar
fig.add_trace(go.Bar(
    name="100% Human Cost",
    x=categories,
    y=[baseline_human, 0],
    marker_color="#90CAF9"
))

# 2a) Hybrid: residual human cost (the un-automated portion)
fig.add_trace(go.Bar(
    name=f"{int((1-automation_pct)*100)}% Human",
    x=categories,
    y=[0, residual_cost],
    marker_color="#64B5F6"
))

# 2b) Hybrid: AI usage cost
fig.add_trace(go.Bar(
    name=f"{int(automation_pct*100)}% AI Usage",
    x=categories,
    y=[0, ai_cost],
    marker_color="#1E88E5"
))

# 2c) Hybrid: Subscription fee
fig.add_trace(go.Bar(
    name="Subscription",
    x=categories,
    y=[0, subscription],
    marker_color="#FFA726"
))

# Layout tweaks
fig.update_layout(
    barmode="stack",
    yaxis_title="Monthly Spend ($)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    margin=dict(t=40, b=20, l=0, r=0),
    **TRANSPARENT
)

st.plotly_chart(fig, use_container_width=True)

# --- 4) Savings Breakdown + Cards ---
st.markdown("---")
st.subheader("💸 Savings Breakdown")
left, right = st.columns([3,1], gap="large")

with left:
    fig_s = go.Figure()
    fig_s.add_trace(go.Bar(
        name="Net Savings", x=["Savings"], y=[net_savings], marker_color="#66BB6A"
    ))
    if include_indirect:
        fig_s.add_trace(go.Bar(
            name="Indirect Sav.", x=["Savings"], y=[indirect_savings], marker_color="#FFA726"
        ))
    if include_hr:
        fig_s.add_trace(go.Bar(
            name="HR Strategic", x=["Savings"], y=[hr_savings], marker_color="#29B6F6"
        ))
    fig_s.update_layout(
        barmode="stack",
        yaxis_title="Monthly Savings ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=40, b=20, l=0, r=0),
        **TRANSPARENT
    )
    st.plotly_chart(fig_s, use_container_width=True)

with right:
    st.markdown("<div class='savings-cards'>", unsafe_allow_html=True)
    st.markdown(card("Net Savings",   f"${net_savings:,.0f}"),    unsafe_allow_html=True)
    if include_indirect:
        st.markdown(card("Indirect Sav.", f"${indirect_savings:,.0f}"),unsafe_allow_html=True)
    if include_hr:
        st.markdown(card("HR Strategic", f"${hr_savings:,.0f}"),     unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 5) Integration Metrics ---
st.markdown("---")
st.subheader("💼 Integration Basis Metrics")
i1,i2,i3,i4 = st.columns(4, gap="large")
i1.markdown(card("ROI on Integration (mo)", f"{roi_int_mo:.1f}%"),  unsafe_allow_html=True)
i2.markdown(card("ROI on Integration (yr)", f"{roi_int_yr:.1f}%"),  unsafe_allow_html=True)
i3.markdown(card("Payback on Int (mo)",   f"{payback_int:.1f} mo"),unsafe_allow_html=True)
i4.markdown(card("Value Basis",           f"${value_prod:,.0f}"),unsafe_allow_html=True)
