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

# ─── Human vs AI Cost Comparison ───────────────────────────────
st.markdown("## 💰 Human vs AI Cost Comparison")
fig_hum_ai = go.Figure(data=[
    go.Bar(
        name="100% Human Cost",
        x=["Cost"],
        y=[baseline_human],
        marker_color="#90CAF9"
    ),
    go.Bar(
        name="100% AI Cost",
        x=["Cost"],
        y=[ai_enabled_cost],
        marker_color="#1E88E5"
    )
])
fig_hum_ai.update_layout(
    barmode='group',
    xaxis=dict(showticklabels=False),
    yaxis_title="Monthly Spend ($)",
    margin=dict(t=30, b=30, l=0, r=0),
    **TRANSPARENT
)
st.plotly_chart(fig_hum_ai, use_container_width=True)


# ─── Savings Breakdown ───────────────────────────────
st.markdown("## 💸 Savings Breakdown")

# two‐column: left = savings bar, right = metric cards
left2, right2 = st.columns([3,1], gap="large")

with left2:
    fig_save = go.Figure(data=[
        go.Bar(
            name="Net Savings",
            x=["Savings"],
            y=[net_savings],
            marker_color="#66BB6A"
        )
    ])
    # add indirect & strategic as stacked pieces if you like:
    if use_indirects:
        fig_save.add_trace(go.Bar(
            name="Indirect Sav.",
            x=["Savings"],
            y=[indirect_savings],
            marker_color="#FFA726"
        ))
    if include_strategic:
        fig_save.add_trace(go.Bar(
            name="HR Strategic",
            x=["Savings"],
            y=[strategic_savings],
            marker_color="#29B6F6"
        ))

    fig_save.update_layout(
        barmode='stack',
        xaxis=dict(showticklabels=False),
        yaxis_title="Monthly Savings ($)",
        margin=dict(t=30, b=30, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        **TRANSPARENT
    )
    st.plotly_chart(fig_save, use_container_width=True)

with right2:
    # vertically stack your three cards
    st.markdown("<div style='display:flex;flex-direction:column;gap:10px;'>",
                unsafe_allow_html=True)
    # Net Savings
    st.markdown(metric_block("Net Savings", net_savings, prefix="$"), unsafe_allow_html=True)
    # Indirect Savings (toggle)
    if use_indirects:
        st.markdown(metric_block("Indirect Sav.", indirect_savings, prefix="$"),
                    unsafe_allow_html=True)
    # Strategic HR Savings (toggle)
    if include_strategic:
        st.markdown(metric_block("HR Strategic", strategic_savings, prefix="$"),
                    unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
