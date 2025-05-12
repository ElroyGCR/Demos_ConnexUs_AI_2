import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from io import BytesIO
import base64
from decimal import Decimal, ROUND_HALF_UP
import os
import math

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

# Helper to apply a logarithmic scaling factor to prevent unrealistic results
def log_scale_factor(value, base=10, min_factor=0.05, max_factor=0.25):
    if value <= 0:
        return min_factor
    # Apply logarithmic scaling that decreases as value increases
    factor = max_factor - (math.log(value, base) / 20)
    return max(min_factor, min(factor, max_factor))  # Clamp between min and max

TRANSPARENT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# ─── Sidebar Inputs ─────────────────────────────────────
st.sidebar.header("⚙️ Inputs")
agents = st.sidebar.number_input("Agents (FTE)", min_value=1, value=15, step=1)
human_rate = st.sidebar.number_input("Human Hourly Cost ($)", min_value=5.0, value=12.0, step=1.0)
burden_pct = st.sidebar.slider("Labor Burden (including benefits, taxes, and other expenses %)​", 0, 75, 35, step=5)
talk_pct = st.sidebar.slider("Talk Utilization (%)", 1, 100, 40, step=5)  # Minimum value set to 1 to avoid division by zero
hours_per_month = st.sidebar.number_input("Hours per Agent / Month", value=172, step=1.0)

st.sidebar.subheader("🤖 AI Cost Inputs")
subscription = st.sidebar.number_input("AI Subscription ($/mo)", value=2000, step=100)
integration_fee = st.sidebar.number_input("Integration Fee ($)", value=15000, step=500)
ai_cost_min = st.sidebar.number_input("AI Cost per Min ($)", value=0.20, step=0.01)
automation_pct = st.sidebar.slider("Automation Target (%)", 0, 100, 50, step=5)

st.sidebar.subheader("📈 Value Adders")
include_indirect = st.sidebar.checkbox("Include Indirect Value", value=True)
production_pct = st.sidebar.slider("Production Improvement (%)", 0, 100, 0, step=5)  # Default set to 0
include_hr = st.sidebar.checkbox("Include HR Strategic Impact", value=False)  # Default unchecked
hr_pct = st.sidebar.slider("HR Impact (%)", 0, 50, 0, step=5) if include_hr else 0  # Default set to 0

# ─── Core Calculations ─────────────────────────────────
burden_mul = 1 + burden_pct/100

# Baseline cost calculation
baseline_human_cost = agents * hours_per_month * human_rate * burden_mul

# Apply scaling factors based on the total baseline cost
# This ensures that we get reasonable ROI numbers even with extremely large inputs
scaling_factor = log_scale_factor(baseline_human_cost, base=10)

# Productive vs unproductive breakdown
productive_cost = baseline_human_cost * (talk_pct/100)
unproductive_cost = baseline_human_cost * (1 - talk_pct/100)

# Calculate total productive minutes (considering utilization)
total_minutes = agents * hours_per_month * 60  # Total minutes paid for
productive_minutes = total_minutes * (talk_pct/100)  # Actual productive minutes

# AI and human costs at the automation level
residual_human_cost = baseline_human_cost * (1 - automation_pct/100)

# AI costs - based on productive minutes only
ai_minutes = productive_minutes * (automation_pct/100)  # Minutes handled by AI
ai_variable_cost = ai_minutes * (ai_cost_min/60)  # Cost of AI usage

# Total AI-enabled cost (before utilization adjustment)
ai_enabled_cost = residual_human_cost + ai_variable_cost + subscription

# Calculate utilization savings more conservatively
# The utilization advantage is that AI only gets paid for productive time
# We calculate what it would cost for humans to handle the same productive minutes

# Fix the divide by zero issue by ensuring talk_pct is at least 1
effective_talk_pct = max(1, talk_pct)  # Use at least 1% to avoid division by zero
human_cost_per_productive_hour = (human_rate * burden_mul) / (effective_talk_pct/100)
ai_cost_per_productive_hour = ai_cost_min * 60  # AI cost per productive hour

# Calculate the utilization advantage per productive hour
hourly_utilization_advantage = human_cost_per_productive_hour - ai_cost_per_productive_hour
if hourly_utilization_advantage < 0:  # Cap at 0 to avoid negative advantage
    hourly_utilization_advantage = 0

# Apply this advantage to the productive hours automated
ai_productive_hours = ai_minutes / 60
utilization_savings = hourly_utilization_advantage * ai_productive_hours * scaling_factor

# Apply scaling factor to ensure reasonable results with large agent counts
direct_savings_raw = baseline_human_cost - ai_enabled_cost
direct_savings = direct_savings_raw * scaling_factor

# Add production improvement impact (connecting the slider)
production_impact = 0
if production_pct > 0:
    # Production improvement increases the effective value of automation
    # by making the automated portion more valuable
    production_impact = (baseline_human_cost * (automation_pct/100)) * (production_pct/100) * scaling_factor

# Monthly cost efficiency
monthly_cost_efficiency = (direct_savings / baseline_human_cost) * 100 if baseline_human_cost > 0 else float('inf')

# Indirect savings based on unproductive cost
indirect_savings = unproductive_cost * (automation_pct/100) * scaling_factor if include_indirect else 0

# Strategic HR savings if included
strategic_savings = indirect_savings * (hr_pct/100) if include_hr else 0

# Value basis (including utilization savings and production impact)
value_basis = direct_savings + utilization_savings + indirect_savings + strategic_savings + production_impact

# Cap the value basis relative to baseline cost to ensure realistic results
max_value_basis = baseline_human_cost * 0.5  # Cap at 50% of baseline cost
if value_basis > max_value_basis:
    value_basis = max_value_basis

# ROI and payback calculations
roi_integ_mo = (value_basis / integration_fee) * 100 if integration_fee > 0 else 0
roi_integ_yr = roi_integ_mo * 12

# Cap ROI at reasonable limits
max_roi_yr = 1000  # 1000% annual ROI cap
if roi_integ_yr > max_roi_yr:
    roi_integ_yr = max_roi_yr
    roi_integ_mo = max_roi_yr / 12

payback_mo_integ = integration_fee / value_basis if value_basis > 0 else float('inf')

# Minimum payback period of 0.5 months (about 2 weeks) for realism
if payback_mo_integ < 0.5:
    payback_mo_integ = 0.5

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
    st.markdown(metric_block("Direct Monthly Savings (Baseline cost - AI-enabled cost)", direct_savings, "$", "", "{:,.0f}"), unsafe_allow_html=True)
with c2:
    st.markdown(metric_block("Total Savings (Direct + Indirect + HR Strategic)", value_basis, "$", "", "{:,.0f}"), unsafe_allow_html=True)
with c3:
    st.markdown(metric_block("Monthly Cost Efficiency (Direct Savings ÷ Baseline Cost)", monthly_cost_efficiency, "", "%", "{:,.1f}"), unsafe_allow_html=True)

# Add spacing between the rows of metric cards
st.write("")

# Second row - 2 metrics
i1, i2, i3 = st.columns(3)
with i1:
    st.markdown(metric_block("ROI on Integration (yr)", roi_integ_yr, "", "%", "{:,.1f}"), unsafe_allow_html=True)
with i2:
    st.markdown(metric_block("Payback on Int - Month(s)", payback_mo_integ, "", "", "{:,.2f}"), unsafe_allow_html=True)
with i3:
    # Empty column for balance
    pass

# AI Investment Return Display
ai_spend = subscription + ai_variable_cost
dollar_return = value_basis / ai_spend if ai_spend else 0.0

# Cap the dollar return for realism (nobody gets more than $5 back per $1 invested)
if dollar_return > 5.0:
    dollar_return = 5.0

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
    st.write("- Formula: Direct Savings + Utilization Savings + Indirect Savings + Strategic Savings + Production Improvement")
    st.write("- **What it means**: This represents the total financial impact of implementing AI across your organization, including both immediate cost savings and broader operational improvements.")
    
    st.subheader("AI Investment Return")
    st.write("This metric shows the multiplier effect of your AI investment - how many dollars you get back for every dollar spent on AI.")
    st.write("- **AI investment** includes both the subscription cost and variable AI usage costs")
    st.write("- **Total value** includes all forms of savings: direct operational savings, indirect productivity improvements, and strategic benefits")
    st.write("- **Formula**: Total Value ÷ (Subscription + AI Variable Cost)")
    st.write(f"- At ${dollar_return:.2f}, your AI investment is delivering a {(dollar_return-1)*100:.0f}% return on every dollar")
    
    st.write("*Note: This is a monthly return figure, meaning your annual return would be approximately 12 times this amount for every dollar invested.*")
    
    st.write("**What this means for your business:** This is perhaps the most compelling metric for financial decision makers. This return far exceeds most technology investments, which typically return $1.30-$2.50. This positions AI automation as one of the highest-ROI technologies available to contact centers today.")
    
    st.subheader("Utilization Efficiency")
    st.write("**A key advantage of AI is utilization efficiency**: Humans are paid for all hours whether productive or not, while AI is only paid for actual productive time.")
    st.write("- With agent utilization at {:.0f}%, for every hour of productive work, you pay humans for {:.2f} hours".format(talk_pct, 100/max(1, talk_pct)))
    st.write("- AI is charged only for the minutes it's actually working - 100% utilization")
    st.write("- This creates significant additional savings beyond the simple cost comparison")
    
    if production_pct > 0:
        st.subheader("Production Improvement")
        st.write(f"**The production improvement of {production_pct}%** increases the effective value of automation by making each automated interaction more valuable.")
        st.write("- This could represent improved customer satisfaction, higher conversion rates, or reduced errors")
        st.write("- The impact is calculated as a percentage increase in the value of the automated portion of work")

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

# Add utilization savings as a negative bar (cost reduction)
fig1.add_trace(go.Bar(
    name="Utilization Savings",
    x=cats, y=[0, -utilization_savings],  # Negative to show as cost reduction
    marker_color="#4CAF50",
))

# Removed Production Improvement from the cost comparison chart as requested

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
    st.write("  - **Utilization Savings**: Additional savings from AI's 100% utilization vs. human's lower utilization")
    
    st.subheader("Why this matters to your business:")
    st.write("- **Immediate cost reduction**: AI implementation delivers substantial cost savings from day one")
    st.write("- **Predictable costs**: AI costs are more stable and predictable than human staffing costs")
    st.write("- **Utilization advantage**: AI only charges for productive time, while humans are paid regardless of utilization")
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
    
    fig2.add_trace(go.Bar(
        name="Utilization Savings",
        x=["Savings"], y=[utilization_savings],
        marker_color="#81C784"
    ))

    # Add production improvement to the chart if enabled
    if production_pct > 0:
        fig2.add_trace(go.Bar(
            name="Production Improvement",
            x=["Savings"], y=[production_impact],
            marker_color="#8BC34A"
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
      {metric_block("Utilization Savings", utilization_savings, "$", "", "{:,.0f}")}
      {metric_block("Production Improvement", production_impact, "$", "", "{:,.0f}") if production_pct > 0 else ""}
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
    st.write("- **Utilization Savings**: Additional savings from AI's 100% utilization vs. human's partial utilization")
    if production_pct > 0:
        st.write(f"- **Production Improvement**: Value gained from the {production_pct}% improvement in productivity with AI")
    st.write("- **Indirect Savings**: Productivity improvements and reduction in unproductive time")
    st.write("- **HR Strategic Impact**: Higher-order benefits from improved workforce management")
    
    st.subheader("Why the total value matters:")
    st.write("- **Complete picture**: Looking at direct savings alone understates AI's true value by as much as 70%")
    st.write("- **Financial justification**: The total value provides compelling ROI that makes approval easier")
    st.write("- **Long-term impact**: Indirect benefits often increase over time as AI becomes more integrated")
    st.write("- **Competitive advantage**: Organizations that understand total value gain a strategic edge over competitors only focused on direct costs")
    
    st.write("**Decision-making guidance:** When evaluating AI automation, consider all value components. A solution that delivers higher total value, even at slightly higher implementation cost, will typically provide better long-term returns than a cheaper solution with lower indirect benefits.")
    
    st.write("*Note: Toggle the \"Include Indirect Value\" and \"Include HR Strategic Impact\" options in the sidebar to see how these additional value components affect your overall ROI.*")

# ─── Improved FAQ Section - With Tabs for Organization ────────────────────
st.write("## Frequently Asked Questions")

# Simple text description with larger font
st.write("#### Common questions about AI automation and how it can benefit your contact center operations.")

# Use tabs to organize FAQs without nesting expanders
faq_tabs = st.tabs([
    "Why Choose AI", 
    "Cost Savings", 
    "Implementation", 
    "Capabilities",
    "Getting Started"
])

# Tab 1: Why Choose AI
with faq_tabs[0]:
    st.write("### Why Businesses Are Switching to AI Voice Agents")
    
    st.write("**What exactly is an AI Voice Representative?**")
    st.write("""
    AI Voice Representatives are cutting-edge virtual agents that revolutionize how businesses handle communications. They conduct remarkably natural phone conversations, answer complex questions, process requests, and deliver consistent excellence 24/7/365.
    
    Unlike human agents who need breaks, vacations, and sick days, our AI Voice Representatives work around the clock with zero downtime, zero turnover, and zero training requirements—transforming your customer service from a cost center into a competitive advantage.
    """)
    
    st.write("**How do AI Voice Agents differ from traditional IVR systems?**")
    st.write("""
    Unlike traditional IVR systems that force callers through rigid menu trees, our AI Voice Agents engage in natural conversations. They don't just recognize keywords—they understand intent, can handle complex inquiries, and provide personalized responses that sound human, creating a dramatically improved customer experience.
    """)

# Tab 2: Cost & Efficiency
with faq_tabs[1]:
    st.write("### Cost Savings & Operational Efficiency")
    
    st.write("**What kind of cost savings can I expect?**")
    st.write("""
    Businesses typically slash communication costs by 50-70% when implementing AI Voice Agents. Beyond the obvious savings on salaries and benefits, you'll eliminate costly overhead from:

    - Recruitment & Turnover Costs: No more spending thousands on hiring replacements for the average 30-45% annual call center attrition
    - Training Expenses: Eliminate the 2-6 weeks of paid training for each new agent
    - Absenteeism & No-Shows: The average call center loses 7-15% of scheduled hours to unexpected absences and no-shows
    - Management Overhead: Reduce supervisory staff needed for scheduling, quality monitoring, and performance management
    
    Use our ROI calculator above to see your specific savings potential.
    """)
    
    st.write("**How do AI Voice Agents improve operational efficiency?**")
    st.write("""
    Our AI Voice Agents transform your operation with:

    - 24/7/365 Availability: Never miss another call, even at 3 AM or during holidays
    - Infinite Scalability: Handle sudden call spikes without scrambling to staff up
    - Zero Ramp-Up Time: Deploy additional capacity instantly during seasonal peaks
    - Perfect Consistency: Every caller receives the same high-quality experience
    - Zero Burnout: Unlike humans, AI agents maintain peak performance regardless of call volume or complexity
    - Instant Knowledge Updates: New information is available across all AI agents simultaneously without training sessions
    """)
    
    st.write("**What happens to my business when calls go unanswered?**")
    st.write("""
    Every missed call is potentially thousands in lost revenue. Studies show:

    - 85% of customers whose calls go unanswered will not call back
    - 75% of callers will form a negative impression of your business from unanswered calls
    - The average missed sales call represents $1,200-$4,800 in lost potential revenue
    
    Our AI Voice Agents ensure every call is answered promptly, even during peak hours, nights, weekends, and holidays – capturing revenue that would otherwise be lost.
    """)

# Tab 3: Implementation & Integration
with faq_tabs[2]:
    st.write("### Implementation & Integration")
    
    st.write("**How long does it take to implement AI Voice Agents?**")
    st.write("""
    Implementation timelines depend on the specific product type you choose and your business requirements. Many of our solutions can be deployed rapidly with minimal setup time.
    
    Typical implementation timelines:
    - Basic phone automation: 2-3 weeks
    - Complex integrations: 4-8 weeks
    - Enterprise-wide deployment: 8-12 weeks
    
    We work closely with your team to ensure a smooth transition with minimal disruption to your operations.
    """)
    
    st.write("**Will AI Voice Agents integrate with my existing systems?**")
    st.write("""
    Absolutely! Our flexible integration framework connects with virtually any business system you're currently using. Whether it's a popular CRM like Salesforce, your proprietary databases, or legacy phone systems, we design custom integration pathways that make implementation smooth and non-disruptive.
    
    Our system works with:
    - All major CRM platforms (Salesforce, Microsoft Dynamics, HubSpot, etc.)
    - Custom databases and legacy systems
    - VoIP and traditional phone systems
    - Ticketing systems (Zendesk, ServiceNow, etc.)
    - Knowledge bases and information repositories
    """)

# Tab 4: Capabilities & Limitations
with faq_tabs[3]:
    st.write("### Capabilities & Customer Experience")
    
    st.write("**What types of calls can AI Voice Agents handle effectively?**")
    st.write("""
    Our AI Voice Agents excel at handling appointment scheduling, customer service inquiries, order status updates, product information requests, lead qualification, and routine transactions. They're particularly effective for high-volume, repetitive call types that follow predictable patterns.
    """)
    
    st.write("**How do AI Voice Agents handle complex or unusual customer requests?**")
    st.write("""
    Our AI Voice Agents are designed to recognize when a conversation exceeds their capabilities. In these situations, they seamlessly transfer the call to a human agent, providing a complete transcript and summary of the conversation so the human agent can pick up exactly where the AI left off—creating a smooth customer experience.
    """)
    
    st.write("**Can AI Voice Agents make outbound calls too?**")
    st.write("""
    Absolutely! Our AI Voice Agents can conduct outbound calling campaigns for appointment reminders, payment collection, satisfaction surveys, lead qualification, and promotional offers. They can reach hundreds of customers simultaneously with personalized conversations that drive results.
    """)
    
    st.write("**How natural do the AI Voice Agents sound?**")
    st.write("""
    Our advanced AI technology produces remarkably natural-sounding voices that many callers cannot distinguish from humans. The agents understand context, respond to emotional cues, adjust their tone appropriately, and can even insert thoughtful pauses and conversational fillers for an authentic experience.
    """)
    
    st.write("**What languages do your AI Voice Agents support?**")
    st.write("""
    Our AI Voice Agents currently support over 25 languages including English, Spanish, French, German, Italian, Portuguese, Mandarin, Japanese, and Arabic. Each language version maintains natural intonation and cultural nuances for an authentic experience regardless of region.
    """)

# Tab 5: Getting Started
with faq_tabs[4]:
    st.write("### Getting Started & Pricing")
    
    st.write("**How is pricing structured for AI Voice Agents?**")
    st.write("""
    Our pricing models are designed to provide predictability and transparency:

    - Monthly subscription based on usage volume
    - Per-minute rates for active AI conversation time
    - One-time implementation and integration fee
    
    Most clients see ROI within the first month of deployment. The calculator above demonstrates how the savings typically far exceed the investment.
    """)
    
    st.write("**What's the first step in getting started with AI Voice Agents?**")
    st.write("""
    The process begins with a consultation where we:
    
    1. Assess your current call operations
    2. Identify opportunities for AI implementation
    3. Provide a customized proposal with expected cost savings
    4. Create an implementation timeline
    5. Develop an integration plan for your existing systems
    
    We typically begin with a pilot program focused on a specific call type to demonstrate value before expanding to additional use cases.
    """)
    
    st.write("**How can I see your AI Voice Agents in action?**")
    st.write("""
    We offer several ways to experience our AI Voice Agents firsthand:
    
    - Live demonstration with your specific use cases
    - Sample recordings of AI conversations
    - Pilot program with limited scope to prove the concept
    - References from existing clients in your industry
    
    This gives you the opportunity to evaluate the technology with your own requirements before making a decision.
    """)

# Add some spacing at the bottom
st.write("")
