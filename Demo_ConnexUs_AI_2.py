import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from io import BytesIO
import base64

# --- Page Setup ---
st.set_page_config(page_title="ConnexUs.AI Calculator",
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
    st.markdown(
        f"""<link rel="icon" type="image/png" sizes="32x32"
                  href="data:image/png;base64,{favicon_b64}">""",
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
            left: 50%;
            transform: translateX(-50%);
            height: 800px;
            width: 850px;
            z-index: 0;
            pointer-events: none;
            background-image: url("data:image/png;base64,{watermark_b64}");
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
            opacity: 0.15;
        }}
        </style>
        <div class="watermark"></div>
        """,
        unsafe_allow_html=True
    )

# --- Global Styles & Layout Helpers ---
TRANSPARENT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

def metric_block(label, value, color="#00FFAA", border="#00FFAA", prefix="", suffix=""):
    return f"""
    <div style='
        background-color: #111;
        border: 2px solid {border};
        border-radius: 12px;
        padding: 15px;
        width: fit-content;
        margin-bottom: 15px;
    '>
        <div style='color: white; font-size: 14px; margin-bottom: 5px;'>{label}</div>
        <div style='color: {color}; font-size: 32px; font-weight: bold;'>
            {prefix}{value:,.1f}{suffix}
        </div>
    </div>
    """

def equal_card(label, value, color="#00FFAA", border="#00FFAA", prefix="", suffix=""):
    return f"""
    <div style="
        flex: 1;
        width: 180px;
        background-color: #111;
        border: 2px solid {border};
        border-radius: 12px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 10px;
    ">
        <div style="color: white; font-size: 14px; margin-bottom: 5px;">{label}</div>
        <div style="color: {color}; font-size: 32px; font-weight: bold;">
            {prefix}{value:,.1f}{suffix}
        </div>
    </div>
    """

# --- Title ---
st.markdown("""
    <div style='padding-top:0;'>
      <h1 style='font-size:2.2rem; font-weight:800; margin-bottom:0.5rem;'>
        ConnexUS AI ROI Calculator
      </h1>
      <hr style='margin-top:0; margin-bottom:1.5rem;'>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR INPUTS ---
st.sidebar.header("🤖 Inputs")

agents = st.sidebar.number_input("Agents (FTE)", min_value=1, value=25, step=1)

human_rate = st.sidebar.number_input("Human Hourly Rate ($)", min_value=1.0,
                                     value=12.0, step=1.0, format="%.2f")

burden = st.sidebar.slider("Burden % (taxes, benefits)", min_value=0, max_value=75,
                           value=35, step=5)

talk_util = st.sidebar.slider("Talk Utilization %", min_value=0, max_value=100,
                              value=40, step=5)

hours_per_month = st.sidebar.number_input("Hours per Agent / Month",
                                          min_value=1.0, value=40*4.33,
                                          step=1.0, format="%.1f")

st.sidebar.markdown("---")
st.sidebar.subheader("💰 AI Cost Inputs")

subscription = st.sidebar.number_input("AI Subscription ($/mo)",
                                       min_value=0, value=2000, step=100)

integration = st.sidebar.number_input("One-time Integration Fee ($)",
                                      min_value=0, value=15000, step=500)

ai_cost_per_min = st.sidebar.number_input("AI Cost per Minute ($)",
                                          min_value=0.0, value=0.20,
                                          step=0.01, format="%.2f")

automation_pct = st.sidebar.slider("Automation % Target",
                                   min_value=0, max_value=100,
                                   value=50, step=5)

st.sidebar.markdown("---")
use_indirects = st.sidebar.checkbox("Include Indirect Value in ROI Calculation",
                                    value=False)
if use_indirects:
    prod_pct = st.sidebar.slider("Prod. Improvement %", 0, 100, 25, step=5)
else:
    prod_pct = 0

include_strategic = st.sidebar.checkbox("Include HR Strategic Savings",
                                        value=False)
if include_strategic:
    strat_pct = st.sidebar.slider("HR Savings %", 0, 50, 10, step=5)
else:
    strat_pct = 0

# --- CALCULATIONS ---
# 1) Workload
total_agent_minutes = agents * hours_per_month * 60
monthly_minutes     = total_agent_minutes * (talk_util / 100)

# 2) Human Baseline Cost
loaded_multiplier   = 1 + burden/100
baseline_human_cost = (monthly_minutes/60) * human_rate * loaded_multiplier

# 3) AI vs Residual
ai_minutes      = monthly_minutes * (automation_pct/100)
residual_minutes = monthly_minutes - ai_minutes

ai_cost         = ai_minutes * ai_cost_per_min
residual_cost   = (residual_minutes/60) * human_rate * loaded_multiplier

ai_enabled_cost = ai_cost + residual_cost + subscription

# 4) Net Savings
net_savings = baseline_human_cost - ai_enabled_cost

# 5) Indirect & Strategic
# indirect = value of productivity regained on the automated minutes
loaded_rate_per_min = (human_rate * loaded_multiplier) / 60
indirect_savings    = ai_minutes * loaded_rate_per_min * (prod_pct/100)

# strategic = simple % of baseline
strategic_savings   = baseline_human_cost * (strat_pct/100)

# 6) Value Basis for ROI
value_basis = net_savings + indirect_savings + strategic_savings

# 7) Operating ROI & Payback (monthly basis)
roi_op_mo   = (value_basis / ai_enabled_cost) * 100 if ai_enabled_cost>0 else 0
roi_op_yr   = roi_op_mo * 12
payback_days= (integration / value_basis)*30 if value_basis>0 else float("inf")

# 8) Integration ROI & Payback
roi_int_mo    = (value_basis / integration)*100 if integration>0 else 0
payback_int_mo= integration / value_basis if value_basis>0 else float("inf")

# 9) $ saved per $1 invested (usage + subscription)
dollars_per_dollar = (value_basis / (ai_cost + subscription)
                      if (ai_cost+subscription)>0 else 0)


# ─── UI: Core Financial Metrics ─────────────────────
st.markdown("## 📊 Core Financial Metrics (Operating Basis)")
col1,col2,col3,col4 = st.columns(4)
with col1:
    st.markdown(metric_block("💰 Net Monthly Savings",
                              net_savings, prefix="$"), unsafe_allow_html=True)
with col2:
    st.markdown(metric_block("💸 Cost Efficiency",
                              (net_savings/baseline_human_cost*100),
                              suffix="%", color="#FFD700", border="#FFD700"),
                  unsafe_allow_html=True)
with col3:
    st.markdown(metric_block("📈 ROI (mo)",
                              roi_op_mo, suffix="%",), unsafe_allow_html=True)
with col4:
    st.markdown(metric_block("📈 ROI (yr)",
                              roi_op_yr, suffix="%",), unsafe_allow_html=True)

st.markdown("---")

# ─── UI: AI Investment Impact ───────────────────────
st.markdown("## 💡 AI Investment Impact")
st.markdown("<div style='color:#DDD;font-size:14px;margin-bottom:8px;'>"
            "Value returned for every $1 spent on AI usage + subscription.</div>",
            unsafe_allow_html=True)
st.markdown(f"""
<div style='
  background-color:#111;
  border:2px solid #00FFAA;
  border-radius:12px;
  padding:15px 25px;
  margin-bottom:25px;
  text-align:center;
'>
  For every <span style='color:#FFD700;font-size:28px;'>$1</span> you invest in AI, you save:
  <span style='color:#00FFAA;font-size:32px;font-weight:700;'>${dollars_per_dollar:,.2f}</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─── Human vs Hybrid Cost Comparison ───────────────────────────────
st.markdown("## 💰 Human vs Hybrid Cost Comparison")

fig = go.Figure()

# Define our two x‐axis categories
cats = ["100% Human", "Hybrid"]

# 1) 100% Human bar (baseline)
fig.add_trace(go.Bar(
    name="100% Human Cost",
    x=cats,
    y=[baseline_human_cost, 0],           # full cost in first column only
    marker_color="#90CAF9",
))

# 2) Hybrid: residual human cost (the % you didn’t automate)
fig.add_trace(go.Bar(
    name=f"{100-automation_pct}% Human",
    x=cats,
    y=[0, residual_cost],                  # only in second column
    marker_color="#64B5F6",
))

# 3) Hybrid: AI Usage cost
fig.add_trace(go.Bar(
    name=f"{automation_pct}% AI Usage",
    x=cats,
    y=[0, ai_cost],                        # only in second column
    marker_color="#1E88E5",
))

# 4) Hybrid: Subscription fee
fig.add_trace(go.Bar(
    name="Subscription",
    x=cats,
    y=[0, subscription],                   # only in second column
    marker_color="#FFAB91",
))

fig.update_layout(
    barmode="stack",
    xaxis_title="",
    yaxis_title="Monthly Spend ($)",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(t=30, b=30, l=0, r=0),
    **TRANSPARENT_LAYOUT
)

st.plotly_chart(fig, use_container_width=True)

# ─── UI: Savings Breakdown ──────────────────────────
st.markdown("## 💸 Savings Breakdown")
left2, right2 = st.columns([3,1], gap="large")

with left2:
    fig_s = go.Figure()
    fig_s.add_trace(go.Bar(
        name="Net Savings",
        x=["Savings"], y=[net_savings],
        marker_color="#66BB6A"
    ))
    if use_indirects:
        fig_s.add_trace(go.Bar(
            name="Indirect Sav.",
            x=["Savings"], y=[indirect_savings],
            marker_color="#FFA726"
        ))
    if include_strategic:
        fig_s.add_trace(go.Bar(
            name="HR Strategic",
            x=["Savings"], y=[strategic_savings],
            marker_color="#29B6F6"
        ))
    fig_s.update_layout(
        barmode="stack",
        xaxis=dict(showticklabels=False),
        yaxis_title="Monthly Savings ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=30, b=30, l=0, r=0),
        **TRANSPARENT_LAYOUT
    )
    st.plotly_chart(fig_s, use_container_width=True)

with right2:
    # stretch cards to match chart height
    st.markdown(
        """<div style="
            display:flex;
            flex-direction:column;
            justify-content:space-between;
            align-items:center;
            height:550px;
        ">""",
        unsafe_allow_html=True
    )
    # always
    st.markdown(equal_card("Net Savings", net_savings, prefix="$"), unsafe_allow_html=True)
    if use_indirects:
        st.markdown(equal_card("Indirect Sav.", indirect_savings, prefix="$"),
                    unsafe_allow_html=True)
    if include_strategic:
        st.markdown(equal_card("HR Strategic", strategic_savings, prefix="$"),
                    unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
