import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from io import BytesIO
import base64
from decimal import Decimal, ROUND_HALF_UP
import os

# ─── Page Setup ────────────────────────────────────────
st.set_page_config(page_title="ConnexUS AI ROI Calculator", layout="wide", page_icon=None)

# ─── Helper to load favicon and watermark ───────────────
def load_base64(path):
    try:
        if not os.path.exists(path):
            st.warning(f"Image file not found: {path}")
            return None
        img = Image.open(path)
        buf = BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    except Exception as e:
        st.warning(f"Error loading image {path}: {str(e)}")
        return None

# Safely handle image loading with fallbacks
try:
    # Try to load favicon with error handling
    favicon_path = "favicon-32x32.png"
    favicon_b64 = load_base64(favicon_path)
    if favicon_b64:
        st.markdown(
            f"""<link rel="icon" href="data:image/png;base64,{favicon_b64}" type="image/png">""",
            unsafe_allow_html=True,
        )
    else:
        # Fallback favicon as base64 encoded string (if the file isn't found)
        st.markdown(
            """<link rel="icon" href="data:image/png;base64,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" type="image/png">""",
            unsafe_allow_html=True,
        )

    # Try to load watermark with error handling
    watermark_path = "connexus_logo_watermark.png"
    watermark_b64 = load_base64(watermark_path)
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
except Exception as e:
    st.warning(f"Error setting up images: {str(e)}")

# ─── CSS Styling ────────────────────────────────────────
st.markdown("""
<style>
  .block-container { padding-top: 1rem !important; }
  .metric-card { background-color: rgba(0,0,0,0.25); border: 2px solid #00FFAA; border-radius: 12px; padding: 15px; text-align:center; }
  .metric-label { color: #DDD; font-size:14px; }
  .metric-value { color: #00FFAA; font-size: 32px; font-weight:bold; }
  
  /* Reduce vertical spacing */
  .reduced-spacing { margin-top: -15px; margin-bottom: -15px; }
  
  /* Logo styling */
  .logo-container {
    margin-bottom: 20px;
    margin-top: 10px;
  }
</style>
""", unsafe_allow_html=True)

# ─── Helpers ───────────────────────────────────────────
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
    return float(Decimal(val).quantize(Decimal('1.' + '0' * decimals), rounding=ROUND_HALF_UP))

TRANSPARENT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# ─── Sidebar Inputs ─────────────────────────────────────
st.sidebar.header("⚙️ Inputs")
agents = st.sidebar.number_input("Agents (FTE)", min_value=1, value=15, step=1)
human_rate = st.sidebar.number_input("Human Hourly Cost ($)", min_value=5.0, value=12.0, step=1.0)
burden_pct = st.sidebar.slider("Labor Burden (including benefits, taxes, and other expenses %)​", 0, 75, 35, step=5)
talk_pct = st.sidebar.slider("Talk Utilization (%)", 0, 100, 40, step=5)
hours_per_month = st.sidebar.number_input("Hours per Agent / Month", value=173.2, step=1.0)

st.sidebar.subheader("🤖 AI Cost Inputs")
subscription = st.sidebar.number_input("AI Subscription ($/mo)", value=2000, step=100)
integration_fee = st.sidebar.number_input("Integration Fee ($)", value=15000, step=500)
ai_cost_min = st.sidebar.number_input("AI Cost per Min ($)", value=0.20, step=0.01)
# Add the AI Amplifier slider
ai_amplifier = st.sidebar.slider("AI Efficiency Amplifier", 0.0, 10.0, 2.0, step=0.5, 
                                help="How many times more efficient AI is compared to humans. Higher values mean AI can do more work at lower cost.")
automation_pct = st.sidebar.slider("Automation Target (%)", 0, 100, 50, step=5)

st.sidebar.subheader("📈 Value Adders")
include_indirect = st.sidebar.checkbox("Include Indirect Value", value=True)
production_pct = st.sidebar.slider("Production Improvement (%)", 0, 100, 25, step=5)
include_hr = st.sidebar.checkbox("Include HR Strategic Impact", value=False)
hr_pct = st.sidebar.slider("HR Impact (%)", 0, 50, 10, step=5) if include_hr else 0

# ─── Core Calculations ─────────────────────────────────
burden_mul = 1 + burden_pct/100

# Baseline cost calculation
baseline_human_cost = agents * hours_per_month * human_rate * burden_mul

# Productive vs unproductive breakdown
productive_cost = baseline_human_cost * (talk_pct/100)
unproductive_cost = baseline_human_cost * (1 - talk_pct/100)

# AI efficiency factor - Using the slider value instead of hardcoded 2.0
ai_efficiency_factor = ai_amplifier if ai_amplifier > 0 else 0.1  # Ensure we don't divide by zero

# AI and human costs at the automation level
residual_human_cost = baseline_human_cost * (1 - automation_pct/100)

# AI cost based on talk time (productive time), adjusted for efficiency
# More efficient means AI costs less to do the same amount of work
ai_variable_cost = (productive_cost * (automation_pct/100)) / ai_efficiency_factor

# Total AI-enabled cost
ai_enabled_cost = residual_human_cost + ai_variable_cost + subscription

# Net savings (renamed to Direct savings in the UI)
direct_savings = baseline_human_cost - ai_enabled_cost

# Monthly cost efficiency
monthly_cost_efficiency = (direct_savings / baseline_human_cost) * 100 if baseline_human_cost > 0 else float('inf')

# Indirect savings based on unproductive cost, enhanced by AI efficiency
# AI efficiency means greater impact on reducing unproductive time
indirect_savings = unproductive_cost * (automation_pct/100) * ai_efficiency_factor if include_indirect else 0

# Strategic HR savings if included
strategic_savings = indirect_savings * (hr_pct/100) if include_hr else 0

# Value basis
value_basis = direct_savings + indirect_savings + strategic_savings

# ROI and payback calculations
roi_integ_mo = (value_basis / integration_fee) * 100 if integration_fee > 0 else 0
roi_integ_yr = roi_integ_mo * 12
payback_mo_integ = integration_fee / value_basis if value_basis > 0 else float('inf')

roi_prod_mo = (value_basis / baseline_human_cost) * 100 if baseline_human_cost > 0 else 0
payback_mo_prod = baseline_human_cost / value_basis if value_basis > 0 else float('inf')

# ─── Logo Display ────────────────────────────────────────
# Load and display the ConnexUS logo in the top left corner
logo_path = "connexus_logo.png"
logo_b64 = load_base64(logo_path)
if logo_b64:
    st.markdown(f"""
    <div class="logo-container">
        <img src="data:image/png;base64,{logo_b64}" style="height:50px;" alt="ConnexUS Logo">
    </div>
    """, unsafe_allow_html=True)
else:
    # If logo not found, display text version
    st.markdown('<div class="logo-container"><span style="font-size:24px; font-weight:bold; color:#00FFAA;">ConnexUS</span></div>', unsafe_allow_html=True)

# ─── ROI Metrics & Investment Impact Section ──────────────────────────
st.write("## ROI Metrics & Investment Impact")

st.write("These key metrics show your cost savings and the value returned for every dollar invested in AI automation.")

# First row - 3 metrics
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(metric_block("Direct Monthly Savings", direct_savings, "$", "", "{:,.0f}"), unsafe_allow_html=True)
with c2:
    st.markdown(metric_block("Total Value (Combined savings)", value_basis, "$", "", "{:,.0f}"), unsafe_allow_html=True)
with c3:
    st.markdown(metric_block("Monthly Cost Efficiency", monthly_cost_efficiency, "", "%", "{:,.1f}"), unsafe_allow_html=True)

# Add spacing between the rows of metric cards
st.write("")

# Second row - 2 metrics
i1, i2, i3 = st.columns(3)
with i1:
    st.markdown(metric_block("ROI on Integration (yr)", roi_integ_yr, "", "%", "{:,.1f}"), unsafe_allow_html=True)
with i2:
    st.markdown(metric_block("Payback on Int (month(s))", payback_mo_integ, "", "", "{:,.2f}"), unsafe_allow_html=True)
with i3:
    # Empty column for balance
    pass

# AI Investment Return Display
ai_spend = subscription + ai_variable_cost
dollar_return = value_basis / ai_spend if ai_spend else 0.0

st.markdown(f"""
<div style='
    background-color: rgba(0,0,0,0.25);
    border: 2px solid #00FFAA;
    border-radius: 12px;
    padding: 15px 30px;
    margin-top: 15px;
    margin-bottom: 15px;
    color: white;
    font-size: 30px;
    font-weight: 500;
    text-align: center;
'>
    For every <span style="color:#FFD700; font-size:46px; font-weight:800;">$1</span> you invest in AI, you save:
    <span style="color:#00FFAA; font-size:50px; font-weight:900;">${dollar_return:,.2f}</span>
</div>
""", unsafe_allow_html=True)

# Combined expander for detailed explanation of both metrics and ROI calculation
with st.expander("ℹ️ How are these metrics calculated?"):
    st.subheader("Direct Savings Metrics")
    st.write("**Direct Monthly Savings**: The total monthly cost reduction achieved by implementing AI.")
    st.write("- Calculated as: Baseline human cost minus AI-enabled cost")
    st.write("- Formula: Agents × Hours × Rate × Burden - (Remaining Human Cost + AI Cost + Subscription)")
    
    st.write("**Monthly Cost Efficiency**: The percentage of baseline costs saved through AI implementation.")
    st.write("- Formula: Direct Savings ÷ Baseline Cost × 100")
    st.write("- **What it means**: Higher percentages indicate greater cost reduction. This directly improves margin and profitability.")
    
    st.subheader("ROI Metrics")
    st.write("**ROI on Integration (yr)**: Annual return on investment relative to your upfront integration costs.")
    st.write("- Shows how quickly you'll recover the initial integration fee")
    st.write("- Formula: (Total Value × 12) ÷ Integration Fee × 100")
    st.write("- **What it means**: Higher percentages indicate faster recovery of integration costs. You're seeing exceptional returns on your integration investment.")
    
    st.subheader("Payback Metrics")
    st.write("**Payback on Integration**: Number of months required to recover your integration investment.")
    st.write("- Formula: Integration Fee ÷ Total Value")
    st.write("- **What it means**: Lower numbers indicate faster ROI. You'll recover your entire integration investment in less than a month - far better than most technology investments which typically take 6-18 months.")
    
    st.subheader("Total Value")
    st.write("**Total Value (Combined)**: The combined total of all direct and indirect savings.")
    st.write("- Formula: Direct Savings + Indirect Savings + Strategic Savings")
    st.write("- **What it means**: This represents the total financial impact of implementing AI across your organization, including both immediate cost savings and broader operational improvements.")
    
    st.subheader("AI Investment Return")
    st.write("This metric shows the multiplier effect of your AI investment - how many dollars you get back for every dollar spent on AI.")
    st.write("- **AI investment** includes both the subscription cost and variable AI usage costs")
    st.write("- **Total value** includes all forms of savings: direct operational savings, indirect productivity improvements, and strategic benefits")
    st.write("- **Formula**: Total Value ÷ (Subscription + AI Variable Cost)")
    st.write(f"- At ${dollar_return:.2f}, your AI investment is delivering a {(dollar_return-1)*100:.0f}% return on every dollar")
    
    st.write("*Note: This is a monthly return figure, meaning your annual return would be approximately 12 times this amount for every dollar invested.*")
    
    st.write("**What this means for your business:** This is perhaps the most compelling metric for financial decision makers. This return far exceeds most technology investments, which typically return $1.30-$2.50. This positions AI automation as one of the highest-ROI technologies available to contact centers today.")

# ─── Human vs Hybrid Cost Comparison ───────────────────
st.write("## Human vs Hybrid Cost Comparison")

# Added explanatory text with consistent formatting
st.write("This chart shows how your current human-only approach compares to a hybrid model with AI automation.")

fig1 = go.Figure()
cats = ["100% Human", "Hybrid"]

fig1.add_trace(go.Bar(
    name="100% Human Cost",
    x=cats, y=[baseline_human_cost, 0],
    marker_color="#90CAF9",
))

fig1.add_trace(go.Bar(
    name=f"{100-automation_pct}% Human",
    x=cats, y=[0, residual_human_cost],
    marker_color="#64B5F6",
))

fig1.add_trace(go.Bar(
    name=f"{automation_pct}% AI Usage",
    x=cats, y=[0, ai_variable_cost],
    marker_color="#1E88E5",
))

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
    height=350,  # Reduced height
    **TRANSPARENT_LAYOUT
)
st.plotly_chart(fig1, use_container_width=True)

# Add toggle for detailed explanation of cost comparison
with st.expander("ℹ️ How to read this cost comparison"):
    st.subheader("Understanding the Cost Comparison")
    st.write("This chart shows the financial difference between your current all-human operation and the proposed AI-hybrid model:")
    st.write("- **Left bar (100% Human)**: Your current monthly spend on human agents")
    st.write("- **Right bar (Hybrid)**: The combined costs of your new hybrid model:")
    st.write("  - **Remaining Human**: Remaining human agent costs")
    st.write("  - **AI Usage**: Variable AI costs based on usage")
    st.write("  - **Subscription**: Fixed monthly AI platform fee")
    
    st.subheader("Why this matters to your business:")
    st.write("- **Immediate cost reduction**: AI implementation delivers substantial cost savings from day one")
    st.write("- **Predictable costs**: AI costs are more stable and predictable than human staffing costs")
    st.write("- **Scalability**: AI can easily scale up or down without the hiring/firing cycles of traditional contact centers")
    st.write("- **Reduced fixed costs**: Converting fixed costs (full-time employees) to variable costs (AI usage) improves financial flexibility")
    st.write("- **Lower operational risk**: AI reduces dependency on labor market conditions and staffing challenges")
    
    st.write("While maintaining the same service capacity, you're able to operate at a significantly lower cost base - this directly improves EBITDA and gives you competitive pricing advantages in your market.")

# ─── Savings Breakdown ─────────────────────────────────
st.write("## Savings Breakdown")

# Added explanatory text with consistent formatting
st.write("This breakdown shows direct savings from AI automation alongside indirect benefits from efficiency improvements.")

left, right = st.columns([3, 1], gap="medium")

with left:
    fig2 = go.Figure()
    
    fig2.add_trace(go.Bar(
        name="Direct Savings",
        x=["Savings"], y=[direct_savings],
        marker_color="#66BB6A"
    ))

    if include_indirect:
        fig2.add_trace(go.Bar(
            name="Indirect Savings",
            x=["Savings"], y=[indirect_savings],
            marker_color="#FFA726"
        ))

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
        height=350,  # Reduced height
        **TRANSPARENT_LAYOUT
    )

    st.plotly_chart(fig2, use_container_width=True)

with right:
    html = f"""
    <div style='
        display: flex;
        flex-direction: column;
        row-gap: 10px;
        margin-top: 10px;
    '>
      {metric_block("Direct Savings", direct_savings, "$", "", "{:,.0f}")}
      {metric_block("Indirect Savings", indirect_savings, "$", "", "{:,.0f}") if include_indirect else ""}
      {metric_block("HR Strategic", strategic_savings, "$", "", "{:,.0f}") if include_hr else ""}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# Add toggle for detailed explanation of savings breakdown
with st.expander("ℹ️ Understanding the savings breakdown"):
    st.subheader("Total Monthly Value")
    st.write("This stacked chart shows how your total monthly value is composed of different types of savings:")
    st.write("- **Direct Savings**: Direct operational cost reduction from implementing AI")
    st.write("- **Indirect Savings**: Productivity improvements and reduction in unproductive time")
    st.write("- **HR Strategic Impact**: Higher-order benefits from improved workforce management")
    
    st.subheader("Why the total value matters:")
    st.write("- **Complete picture**: Looking at direct savings alone understates AI's true value by as much as 70%")
    st.write("- **Financial justification**: The total value provides compelling ROI that makes approval easier")
    st.write("- **Long-term impact**: Indirect benefits often increase over time as AI becomes more integrated")
    st.write("- **Competitive advantage**: Organizations that understand total value gain a strategic edge over competitors only focused on direct costs")
    
    st.write("**Decision-making guidance:** When evaluating AI automation, consider all three value components. A solution that delivers higher total value, even at slightly higher implementation cost, will typically provide better long-term returns than a cheaper solution with lower indirect benefits.")
    
    st.write("*Note: Toggle the \"Include Indirect Value\" and \"Include HR Strategic Impact\" options in the sidebar to see how these additional value components affect your overall ROI.*")

# ─── Absolute Minimum FAQ Section ────────────────────
# Using only the most basic Streamlit components and no HTML

# Simple header using st.write instead of markdown
st.write("## Frequently Asked Questions")

# Simple text description with larger font
st.write("#### Common questions about AI automation and how it can benefit your contact center operations.")

# Simple button-like text
st.success("➕ For detailed FAQs, please visit www.connexus.ai")

# Add just a few sample questions as plain text
st.write("**What exactly is an AI Voice Representative?**")
st.write("AI Voice Representatives are cutting-edge virtual agents that revolutionize how businesses handle communications. They conduct remarkably natural phone conversations, answer complex questions, process requests, and deliver consistent excellence 24/7/365.")

st.write("**What kind of cost savings can I expect?**")
st.write("Businesses typically slash communication costs by 50-70% when implementing AI Voice Agents, eliminating costly overhead from recruitment, training, absenteeism, and management.")

# Add spacing at the bottom
st.write("")
