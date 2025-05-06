import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from io import BytesIO
import base64

# --- Page setup & favicon ----------------------------------
st.set_page_config(
    page_title="ConnexUS AI ROI Calculator",
    page_icon="favicon-32x32.png",
    layout="wide"
)

def _load_base64(path):
    try:
        img = Image.open(path)
        buf = BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    except:
        return None

favicon_b64 = _load_base64("favicon-32x32.png")
if favicon_b64:
    st.markdown(f"""
        <link rel="icon" type="image/png" sizes="32x32"
              href="data:image/png;base64,{favicon_b64}" />
    """, unsafe_allow_html=True)

# --- Transparent layout for all Plotly charts -------------
TRANSPARENT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

# --- Metric card helper -----------------------------------
def metric_card(label, value, prefix="$", suffix="", decimals=2):
    fmt = f"{{:,.{decimals}f}}"
    return f"""
    <div style='
        border: 2px solid #00FFAA;
        border-radius: 8px;
        padding:12px 16px;
        text-align:center;
        background-color:#111;
    '>
      <div style='color:#AAA; font-size:14px; margin-bottom:4px;'>{label}</div>
      <div style='color:#00FFAA; font-size:28px; font-weight:bold;'>
        {prefix}{fmt.format(value)}{suffix}
      </div>
    </div>
    """

# --- Watermark --------------------------------------------
watermark_b64 = _load_base64("connexus_logo_watermark.png")
if watermark_b64:
    st.markdown(f"""
    <style>
    .watermark {{
      position:fixed; top:80px; left:50%;
      transform:translateX(-50%);
      width:800px; height:800px;
      opacity:0.15; z-index:0;
      background:url("data:image/png;base64,{watermark_b64}") 
                 no-repeat center/contain;
      pointer-events:none;
    }}
    </style>
    <div class="watermark"></div>
    """, unsafe_allow_html=True)

# --- Header ------------------------------------------------
st.markdown("""
    <h1 style='font-size:2.2rem; font-weight:800; margin-bottom:0.25rem;'>
      🚀 ConnexUS AI ROI Calculator
    </h1>
    <hr style='margin-bottom:1.5rem;'>
""", unsafe_allow_html=True)

# --- SIDEBAR: Inputs ---------------------------------------
st.sidebar.header("🤖 AI vs Human Inputs")

agents    = st.sidebar.number_input("Agents (FTE)", min_value=1, value=25)
hourly    = st.sidebar.number_input("Human Hourly Rate ($)", min_value=5, max_value=50, value=12)
burden    = st.sidebar.slider("Burden (taxes & benefits %)", 0.0, 0.75, 0.35, step=0.05)
util      = st.sidebar.slider("Talk Utilization (%)", 0.0, 1.0, 0.40, step=0.05)
hrs_month = st.sidebar.number_input("Hours per Agent / Month", value=173.2)

st.sidebar.markdown("---")
subscription     = st.sidebar.number_input("AI Monthly Subscription ($)", value=2000)
integration_fee  = st.sidebar.number_input("One-time Integration Fee ($)", value=15000)
ai_cost_per_min  = st.sidebar.number_input("AI Cost per Minute ($)", value=0.20)
automation       = st.sidebar.slider("Automation Target (%)", 0, 100, 25, step=5)
use_indirects    = st.sidebar.checkbox("Include Indirect Savings", value=True)
include_strategic= st.sidebar.checkbox("Include HR-Strategic Savings", value=False)

# --- 1) Derived variables -----------------------------------
automation_pct       = automation / 100.0
monthly_minutes      = agents * util * hrs_month * 60
ai_minutes           = monthly_minutes * automation_pct
residual_minutes     = monthly_minutes - ai_minutes

# Raw cost numbers
ai_cost              = ai_minutes * ai_cost_per_min
residual_cost        = (residual_minutes / 60) * hourly * (1 + burden)
subscription_cost    = subscription

# Combined AI+humans cost
hybrid_cost          = ai_cost + residual_cost + subscription_cost

# Baseline human-only cost
baseline_human_cost  = agents * hrs_month * hourly * (1 + burden)

# Direct savings
net_savings          = baseline_human_cost - hybrid_cost

# Indirect (production & upsell) — as a % of saved labor cost
indirect_savings     = net_savings * 0.25 if use_indirects else 0.0

# HR-Strategic (attrition, recruitment) assumed 0–50% of net_savings
strategic_savings    = net_savings * 0.15 if include_strategic else 0.0

# Value basis for ROI
value_basis          = net_savings + indirect_savings + strategic_savings

# ROI / Payback metrics
roi_prod_mo          = (value_basis / hybrid_cost) * 100 if hybrid_cost else 0
payback_prod_mo      = (hybrid_cost / value_basis) if value_basis else float("inf")

roi_int_mo           = (value_basis / integration_fee) * 100 if integration_fee else 0
payback_int_mo       = (integration_fee / value_basis) if value_basis else float("inf")

# $1→Savings
dollar_return        = value_basis / (subscription + ai_cost) if (subscription + ai_cost)>0 else 0

# --- 2) Core Financial Metrics -----------------------------
st.subheader("📊 Core Financial Metrics")
c1,c2,c3,c4 = st.columns(4, gap="large")
c1.markdown(metric_card("Net Monthly Savings", net_savings), unsafe_allow_html=True)
c2.markdown(metric_card("ROI on Prod (mo)", roi_prod_mo, suffix="%", decimals=1), unsafe_allow_html=True)
c3.markdown(metric_card("Payback on Prod (mo)", payback_prod_mo, prefix="$", decimals=2), unsafe_allow_html=True)
c4.markdown(metric_card("$1 → Savings", dollar_return, prefix="$", decimals=2), unsafe_allow_html=True)

# --- 3) AI Investment Impact -------------------------------
st.markdown("---")
st.subheader("💡 AI Investment Impact")
st.markdown(
    "<div style='color:#DDD;font-size:14px;margin-bottom:8px;'>"
    "Value returned for every $1 spent on AI usage + subscription."
    "</div>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div style='
      border:2px solid #00FFAA; border-radius:12px;
      padding:16px; background:#111; text-align:center;
    '>
      <span style='font-size:20px;'>For every </span>
      <span style='font-size:32px; color:#FFD700; font-weight:bold;'>$1</span>
      <span style='font-size:20px;'> you invest in AI, you save:</span>
      <span style='font-size:32px; color:#00FFAA; font-weight:bold;'>
        ${dollar_return:,.0f}
      </span>
    </div>
    """,
    unsafe_allow_html=True
)

# --- 4) Integration Basis Metrics --------------------------
st.markdown("---")
st.subheader("💼 Integration Basis Metrics")
i1,i2,i3,i4 = st.columns(4, gap="large")
i1.markdown(metric_card("ROI on Integration (mo)", roi_int_mo, suffix="%", decimals=1),
            unsafe_allow_html=True)
i2.markdown(metric_card("ROI on Integration (yr)", roi_int_mo*12, suffix="%", decimals=1),
            unsafe_allow_html=True)
i3.markdown(metric_card("Payback on Int (mo)", payback_int_mo, suffix="mo", decimals=2),
            unsafe_allow_html=True)
i4.markdown(metric_card("Value Basis", value_basis), unsafe_allow_html=True)

# --- 5) Human vs Hybrid Cost Comparison --------------------
st.markdown("---")
st.subheader("💰 Human vs Hybrid Cost Comparison")

cats = ["100% Human", "Hybrid"]
fig = go.Figure()

fig.add_trace(go.Bar(
    name="100% Human Cost",
    x=cats, y=[baseline_human_cost, 0],
    marker_color="#90CAF9"
))
fig.add_trace(go.Bar(
    name=f"{int((1-automation_pct)*100)}% Human",
    x=cats, y=[0, residual_cost],
    marker_color="#64B5F6"
))
fig.add_trace(go.Bar(
    name=f"{int(automation_pct*100)}% AI Usage",
    x=cats, y=[0, ai_cost],
    marker_color="#1E88E5"
))
fig.add_trace(go.Bar(
    name="Subscription",
    x=cats, y=[0, subscription_cost],
    marker_color="#FFA726"
))

fig.update_layout(
    barmode="stack",
    yaxis_title="Monthly Spend ($)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    margin=dict(t=40, b=20, l=40, r=20),
    **TRANSPARENT
)
st.plotly_chart(fig, use_container_width=True)

# --- 6) Savings Breakdown ----------------------------------
st.markdown("---")
st.subheader("💸 Savings Breakdown")
left, right = st.columns([3,1], gap="large")

with left:
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        name="Net Savings",
        x=["Savings"], y=[net_savings],
        marker_color="#66BB6A"
    ))
    if use_indirects:
        fig2.add_trace(go.Bar(
            name="Indirect Sav.",
            x=["Savings"], y=[indirect_savings],
            marker_color="#FFA726"
        ))
    if include_strategic:
        fig2.add_trace(go.Bar(
            name="HR Strategic",
            x=["Savings"], y=[strategic_savings],
            marker_color="#29B6F6"
        ))

    fig2.update_layout(
        barmode="stack",
        yaxis_title="Monthly Savings ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=40, b=20, l=40, r=20),
        **TRANSPARENT
    )
    st.plotly_chart(fig2, use_container_width=True)

with right:
    st.markdown("<div style='display:flex; flex-direction:column; gap:12px;'>",
                unsafe_allow_html=True)
    st.markdown(metric_card("Net Savings", net_savings), unsafe_allow_html=True)
    if use_indirects:
        st.markdown(metric_card("Indirect Sav.", indirect_savings), unsafe_allow_html=True)
    if include_strategic:
        st.markdown(metric_card("HR Strategic", strategic_savings), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
