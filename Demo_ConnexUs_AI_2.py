import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import plotly.graph_objects as go

# --- Page Setup ---
st.set_page_config(
    page_title="ConnexUS AI ROI Calculator",
    page_icon="favicon-32x32.png",
    layout="wide"
)

# --- Load Base64 (favicon & watermark) ---
def load_base64(path):
    try:
        img = Image.open(path)
        buf = BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    except:
        return None

# Favicon
fav_b64 = load_base64("favicon-32x32.png")
if fav_b64:
    st.markdown(
        f'<link rel="icon" href="data:image/png;base64,{fav_b64}">',
        unsafe_allow_html=True
    )

# Watermark
wm_b64 = load_base64("connexus_logo_watermark.png")
if wm_b64:
    st.markdown(f"""
    <style>
      .watermark {{
        position: fixed; top:80px; left:50%;
        transform: translateX(-50%);
        width:800px; height:800px;
        background: url("data:image/png;base64,{wm_b64}") no-repeat center/contain;
        opacity:0.15; pointer-events:none; z-index:0;
      }}
    </style><div class="watermark"></div>
    """, unsafe_allow_html=True)

# --- Transparent Plotly ---
TRANSPARENT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# --- UI Helper Functions ---
def metric_block(label, val, icon=None, prefix="", suffix="", color="#00FFAA"):
    icon_html = f"<img src='{icon}' width='16' style='vertical-align:middle;margin-right:4px;'/>" if icon else ""
    return f"""
    <div style='display:inline-block;
                background:rgba(17,17,17,0.8);
                border:2px solid {color};
                border-radius:10px;
                padding:10px 20px;
                margin:5px;
                z-index:1;'>
      <div style='color:#DDD; font-size:14px;'>{icon_html}{label}</div>
      <div style='color:{color}; font-size:28px; font-weight:600;'>
        {prefix}{val:,.1f}{suffix}
      </div>
    </div>
    """

def small_card(label, val, prefix="", suffix=""):
    return f"""
    <div style='display:inline-block;
                background:rgba(17,17,17,0.8);
                border:1px solid #00FFAA;
                border-radius:8px;
                padding:6px 12px;
                margin:3px;
                text-align:center;
                z-index:1;'>
      <div style='color:#AAA; font-size:11px;'>{label}</div>
      <div style='color:#00FFAA; font-size:16px; font-weight:600;'>
        {prefix}{val:,.1f}{suffix}
      </div>
    </div>
    """

def caption(txt):
    return f"<div style='color:#DDD; font-size:14px;'>{txt}</div>"

# --- Title ---
st.markdown("""
    <h1 style='color:white; font-size:2.4rem; font-weight:800;
               margin-bottom:0.2rem; z-index:1;'>
      ConnexUS AI ROI Calculator
    </h1>
    <hr style='border-top:1px solid #333;'>
""", unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
st.sidebar.header("📊 Input Your Call Center Data")

# Volume & Handle Time
st.sidebar.subheader("🔄 Volume & Handle Time")
weekly_interactions= st.sidebar.number_input("Weekly Interactions", 1, 100_000, value=10_000, step=100)
aht                = st.sidebar.slider("Avg Handle Time (min)", 1, 20, 6)

# Workforce Metrics
st.sidebar.subheader("👥 Workforce Metrics")
agents             = st.sidebar.number_input("Agents (FTE)", 1, value=25)
hourly_cost        = st.sidebar.number_input("Agent Hourly Cost ($)", 5.0, 100.0, 12.0)
burden_pct         = st.sidebar.slider("Burden % (Tax+Benefits)", 0, 75, 35, step=5)
talk_pct           = st.sidebar.slider("Talk Utilization %", 0, 100, 40, step=5)
hours_per_month    = st.sidebar.number_input("Hrs/Agent per Month", 0.0, 500.0, 40*4.33)

# Business Impact
st.sidebar.subheader("💼 Business Impact")
production_pct     = st.sidebar.number_input("Production Improvement %", 0.0, 100.0, 25.0)

# AI Cost Inputs
st.sidebar.subheader("🤖 AI Cost Inputs")
subscription       = st.sidebar.number_input("AI Subscription ($/mo)", 0, 10_000, 2_000, step=100)
integration_fee    = st.sidebar.number_input("Integration Fee ($)",     0, 100_000, 15_000, step=500)
ai_cost_per_min    = st.sidebar.number_input("AI Cost per Minute ($)", 0.0, 5.0, 0.20, step=0.01)
automation_pct     = st.sidebar.slider("Automation % Target", 0, 100, 50, step=5)

# ROI Toggles
st.sidebar.subheader("⚙️ ROI Options")
use_indirects      = st.sidebar.checkbox("Include Indirect Value",    True)
include_strategic  = st.sidebar.checkbox("Include Strategic HR Sav.", False)
strategic_pct      = st.sidebar.slider("Strategic HR Savings %", 0, 50, 25, step=5) \
                         if include_strategic else 0

# --- CALCULATIONS ---
# 1) Workload in minutes
monthly_minutes    = weekly_interactions * aht * 4.33

# 2) AI vs Residual Costs
ai_minutes         = (automation_pct/100) * monthly_minutes
residual_minutes   = monthly_minutes - ai_minutes
ai_cost            = ai_minutes * ai_cost_per_min
fully_loaded_mul   = 1 + (burden_pct/100)
residual_cost      = (residual_minutes/60) * hourly_cost * fully_loaded_mul
ai_enabled_cost    = ai_cost + residual_cost + subscription

# 3) Indirect (Production) Savings
production_savings = (monthly_minutes * (production_pct/100) /60) \
                     * hourly_cost * fully_loaded_mul
indirect_savings   = production_savings

# 4) Baseline Human Cost
agent_hrs          = hours_per_month
mins_per_agent     = agent_hrs * 60
req_agents         = monthly_minutes / mins_per_agent
eff_agents         = max(agents, req_agents)
baseline_human     = (eff_agents * agent_hrs
                      * hourly_cost * fully_loaded_mul)

# 5) Net Savings
net_savings        = baseline_human - ai_enabled_cost

# 6) Strategic HR Savings
strategic_savings  = net_savings * (strategic_pct/100)

# 7) Value Basis
value_basis        = net_savings
if use_indirects:     value_basis += indirect_savings
if include_strategic: value_basis += strategic_savings

# 8) ROI & Payback (Operating)
roi_monthly        = (value_basis / ai_enabled_cost)*100 \
                     if ai_enabled_cost else 0
payback_mo_op      = (ai_enabled_cost / value_basis) \
                     if value_basis else float('inf')

# 9) ROI & Payback (Integration)
roi_integ_mo       = (value_basis / integration_fee)*100 \
                     if integration_fee else 0
payback_mo_int     = (integration_fee / value_basis) \
                     if value_basis else float('inf')

# 10) Cost Eff & $ saved per $
cost_efficiency    = ((baseline_human - ai_enabled_cost)
                     / baseline_human)*100 \
                     if baseline_human else 0
dollar_saved_per_d = (value_basis / (ai_cost+subscription)) \
                     if (ai_cost+subscription) else 0

# --- DISPLAY METRICS ---
st.markdown("## 📊 Core Financial Metrics")
st.markdown(caption("Savings vs. a fully human operation"))

c1,c2,c3,c4 = st.columns(4)
with c1:
    st.markdown(metric_block("Net Savings", net_savings,
                             icon="favicon-16x16.png", prefix="$"),
                unsafe_allow_html=True)
with c2:
    st.markdown(metric_block("Cost Eff.", cost_efficiency,
                             icon="favicon-16x16.png", suffix="%"),
                unsafe_allow_html=True)
with c3:
    st.markdown(metric_block("ROI Mo", roi_monthly,
                             icon="favicon-16x16.png", suffix="%"),
                unsafe_allow_html=True)
with c4:
    st.markdown(metric_block("Payback Mo", payback_mo_op,
                             icon="favicon-16x16.png", suffix=" mo"),
                unsafe_allow_html=True)

# --- AI INVESTMENT IMPACT BANNER ---
st.markdown("---")
st.markdown("## 💡 AI Investment Impact")
st.markdown(caption(
    "Shows how much value is returned for every dollar spent on AI usage + subscription."
))
st.markdown(f"""
<div style='
    background: rgba(17,17,17,0.8);
    border: 2px solid #00FFAA;
    border-radius:12px;
    padding:20px 30px;
    text-align:center;
    margin:10px 0 30px 0;
    color:white;
    font-size:1.2rem;
'>
  For every
  <span style='color:#FFD700; font-size:2rem; font-weight:800;'>$1</span>
  you invest in AI, you save:
  <span style='color:#00FFAA; font-size:2.5rem; font-weight:900;'>${dollar_saved_per_d:.2f}</span>
</div>
""", unsafe_allow_html=True)

# --- Integration Metrics ---
st.markdown("## 💼 Integration Basis Metrics")
st.markdown(caption("Returns vs. one-time integration fee"))
i1,i2,i3,i4 = st.columns(4)
with i1:
    st.markdown(metric_block("ROI Mo", roi_integ_mo,
                             icon="favicon-16x16.png", suffix="%"),
                unsafe_allow_html=True)
with i2:
    st.markdown(metric_block("ROI Yr", roi_integ_mo*12,
                             icon="favicon-16x16.png", suffix="%"),
                unsafe_allow_html=True)
with i3:
    st.markdown(metric_block("Payback Mo", payback_mo_int,
                             icon="favicon-16x16.png", suffix=" mo"),
                unsafe_allow_html=True)
with i4:
    st.markdown(metric_block("Value Basis", value_basis,
                             icon="favicon-16x16.png", prefix="$"),
                unsafe_allow_html=True)

# --- 3-Column Cost vs. AI vs. Savings (unchanged) ---
st.markdown("---")
st.markdown("## 🏷️ Cost vs. AI vs. Savings")
col1, col2, col3 = st.columns([1,1,1], gap="large")

with col1:
    st.markdown(metric_block("100% Human Cost", baseline_human,
                             icon="favicon-32x32.png", prefix="$"),
                unsafe_allow_html=True)
with col2:
    st.markdown(metric_block(f"AI Cost ({automation_pct}% auto)", ai_enabled_cost,
                             icon="favicon-32x32.png", prefix="$"),
                unsafe_allow_html=True)

# --- New: Chart + Savings Cards Side-by-Side ---
st.markdown("---")
left, right = st.columns([3,1], gap="large")

with left:
    # your existing stacked-bar figure
    fig = go.Figure()
    cats = ["100% Human", f"{automation_pct}% AI", "Savings"]
    # (add your traces exactly as before…)
    # …
    fig.update_layout(
        barmode='stack',
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=40,b=0,l=0,r=0),
        xaxis_title="",
        yaxis_title="Amount ($)",
        **TRANSPARENT
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("<div style='display:flex;flex-direction:column; gap:10px;'>", unsafe_allow_html=True)

    # Always show Net Savings
    st.markdown(small_card("Net Savings", net_savings, prefix="$"), unsafe_allow_html=True)

    # Conditionally show Indirect
    if use_indirects:
        st.markdown(small_card("Indirect Sav.", indirect_savings, prefix="$"),
                    unsafe_allow_html=True)

    # Conditionally show HR Strategic
    if include_strategic:
        st.markdown(small_card("HR Strategic", strategic_savings, prefix="$"),
                    unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# --- Stacked-Bar Chart ---
fig = go.Figure()
# categories on x-axis
cats = ["100% Human", f"{automation_pct}% AI", "Savings"]

# Human cost
fig.add_trace(go.Bar(
    name="Human Cost",
    x=cats, y=[baseline_human, 0, 0],
    marker_color="#90CAF9"
))

# AI cost breakdown
fig.add_trace(go.Bar(
    name="AI Usage",
    x=cats, y=[0, ai_cost, 0],
    marker_color="#1E88E5"
))
fig.add_trace(go.Bar(
    name="Residual Labor",
    x=cats, y=[0, residual_cost, 0],
    marker_color="#64B5F6"
))
fig.add_trace(go.Bar(
    name="Subscription",
    x=cats, y=[0, subscription, 0],
    marker_color="#FFAB91"
))

# Savings
fig.add_trace(go.Bar(
    name="Net Savings",
    x=cats, y=[0, 0, net_savings],
    marker_color="#66BB6A"
))
if use_indirects:
    fig.add_trace(go.Bar(
        name="Indirect Sav.",
        x=cats, y=[0,0,indirect_savings],
        marker_color="#FFA726"
    ))
if include_strategic:
    fig.add_trace(go.Bar(
        name="HR Strategic",
        x=cats, y=[0,0,strategic_savings],
        marker_color="#29B6F6"
    ))

fig.update_layout(
    barmode='stack',
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    margin=dict(t=40,b=0,l=0,r=0),
    xaxis_title="",
    yaxis_title="Amount ($)",
    **TRANSPARENT
)

st.plotly_chart(fig, use_container_width=True)
