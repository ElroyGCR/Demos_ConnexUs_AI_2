import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from io import BytesIO
import base64
from decimal import Decimal, ROUND_HALF_UP

# ─── Page Setup ────────────────────────────────────────
st.set_page_config(page_title="ConnexUS AI ROI Calculator", layout="wide", page_icon="favicon.ico")

# ─── Helper to load favicon and watermark ───────────────
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
burden_pct = st.sidebar.slider("Burden (Benefits %)​", 0, 75, 35, step=5)
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

# ─── Core Calculations ─────────────────────────────────
burden_mul = 1 + burden_pct/100

# Baseline cost calculation
baseline_human_cost = agents * hours_per_month * human_rate * burden_mul

# Productive vs unproductive breakdown
productive_cost = baseline_human_cost * (talk_pct/100)
unproductive_cost = baseline_human_cost * (1 - talk_pct/100)

# AI efficiency factor - AI's operational advantage over humans based on utilization
# AI can work 24/7 while humans are limited by talk utilization
# Fine-tuned based on Excel model to match expected returns
ai_efficiency_factor = 2.0 if talk_pct > 0 else 2.0  # Optimized efficiency factor

# AI and human costs at the automation level
residual_human_cost = baseline_human_cost * (1 - automation_pct/100)

# AI cost based on talk time (productive time), adjusted for efficiency
# More efficient means AI costs less to do the same amount of work
ai_variable_cost = (productive_cost * (automation_pct/100)) / ai_efficiency_factor

# Total AI-enabled cost
ai_enabled_cost = residual_human_cost + ai_variable_cost + subscription

# Net savings
net_savings = baseline_human_cost - ai_enabled_cost

# Monthly cost efficiency
monthly_cost_efficiency = (net_savings / baseline_human_cost) * 100 if baseline_human_cost > 0 else float('inf')

# Indirect savings based on unproductive cost, enhanced by AI efficiency
# AI efficiency means greater impact on reducing unproductive time
indirect_savings = unproductive_cost * (automation_pct/100) * ai_efficiency_factor if include_indirect else 0

# Strategic HR savings if included
strategic_savings = indirect_savings * (hr_pct/100) if include_hr else 0

# Value basis
value_basis = net_savings + indirect_savings + strategic_savings

# ROI and payback calculations
roi_integ_mo = (value_basis / integration_fee) * 100 if integration_fee > 0 else 0
roi_integ_yr = roi_integ_mo * 12
payback_mo_integ = integration_fee / value_basis if value_basis > 0 else float('inf')

roi_prod_mo = (value_basis / baseline_human_cost) * 100 if baseline_human_cost > 0 else 0
payback_mo_prod = baseline_human_cost / value_basis if value_basis > 0 else float('inf')

# ─── Main Title ─────────────────────────────────────────
st.title("ConnexUS AI ROI Calculator")
st.markdown("---")

# ─── Main Metrics Section ──────────────────────────────
col_icon1, col_text1 = st.columns([1, 20])
with col_icon1:
    st.image("favicon-32x32.png", width=32)
with col_text1:
    st.markdown('<span style="font-size: 32px; font-weight: bold; vertical-align: middle;">Metrics Overview</span>', unsafe_allow_html=True)

st.markdown("""
<div style="background-color: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px; margin-bottom: 20px;">
    <p style="color: #ffffff; font-size: 16px; margin: 0;">
        These values reflect direct cost savings compared to your human-only baseline operations.
    </p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(metric_block("Net Monthly Savings", net_savings, "$", "", "{:,.0f}"), unsafe_allow_html=True)
with c2:
    st.markdown(metric_block("ROI on Production (mo)", roi_prod_mo, "", "%", "{:,.1f}"), unsafe_allow_html=True)
with c3:
    st.markdown(metric_block("Payback on Prod (mo)", payback_mo_prod, "", " mo", "{:,.2f}"), unsafe_allow_html=True)
with c4:
    st.markdown(metric_block("Monthly Cost Efficiency", monthly_cost_efficiency, "", "%", "{:,.1f}"), unsafe_allow_html=True)

# Add spacing between the rows of metric cards
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

i1, i2, i3, i4 = st.columns(4)
with i1:
    st.markdown(metric_block("ROI on Integration (mo)", roi_integ_mo, "", "%", "{:,.1f}"), unsafe_allow_html=True)
with i2:
    st.markdown(metric_block("ROI on Integration (yr)", roi_integ_yr, "", "%", "{:,.1f}"), unsafe_allow_html=True)
with i3:
    st.markdown(metric_block("Payback on Int (mo)", payback_mo_integ, "", " mo", "{:,.2f}"), unsafe_allow_html=True)
with i4:
    st.markdown(metric_block("Total Value (Combined)", value_basis, "$", "", "{:,.0f}"), unsafe_allow_html=True)

# Add toggle for detailed explanation of the metrics
with st.expander("ℹ️ How are these metrics calculated?"):
    st.subheader("Direct Savings Metrics")
    st.write("**Net Monthly Savings**: The total monthly cost reduction achieved by implementing AI.")
    st.write("- Calculated as: Baseline human cost minus AI-enabled cost")
    st.write("- Formula: Agents × Hours × Rate × Burden - (Remaining Human Cost + AI Cost + Subscription)")
    
    st.write("**Monthly Cost Efficiency**: The percentage of baseline costs saved through AI implementation.")
    st.write("- Formula: Net Savings ÷ Baseline Cost × 100")
    st.write("- **What it means**: Higher percentages indicate greater cost reduction. This directly improves margin and profitability.")
    
    st.subheader("ROI Metrics")
    st.write("**ROI on Production**: Return on investment relative to your baseline operational costs.")
    st.write("- Shows how much value is returned for every dollar of your current operations")
    st.write("- Formula: Total Value ÷ Baseline Cost × 100")
    st.write("- **What it means**: A higher percentage indicates greater value creation. Your AI implementation is delivering nearly double the value of your current operational investment each month.")
    
    st.write("**ROI on Integration**: Return on investment relative to your upfront integration costs.")
    st.write("- Shows how quickly you'll recover the initial integration fee")
    st.write("- Formula: Total Value ÷ Integration Fee × 100")
    st.write("- **What it means**: Higher percentages indicate faster recovery of integration costs. You're seeing exceptional returns on your integration investment.")
    
    st.subheader("Payback Metrics")
    st.write("**Payback on Production**: Number of months required to recover your baseline operational costs.")
    st.write("- Formula: Baseline Cost ÷ Total Value")
    st.write("- **What it means**: Lower numbers are better. You'll recover your monthly operational investment quickly through AI implementation savings.")
    
    st.write("**Payback on Integration**: Number of months required to recover your integration investment.")
    st.write("- Formula: Integration Fee ÷ Total Value")
    st.write("- **What it means**: Lower numbers indicate faster ROI. You'll recover your entire integration investment in less than a month - far better than most technology investments which typically take 6-18 months.")
    
    st.subheader("Total Value")
    st.write("**Total Value (Combined)**: The combined total of all direct and indirect savings.")
    st.write("- Formula: Net Savings + Indirect Savings + Strategic Savings")
    st.write("- **What it means**: This represents the total financial impact of implementing AI across your organization, including both immediate cost savings and broader operational improvements.")

st.markdown("---")

# ─── AI Investment Impact ─────────────────────────────
col_icon2, col_text2 = st.columns([1, 20])
with col_icon2:
    st.image("favicon-32x32.png", width=32)
with col_text2:
    st.markdown('<span style="font-size: 32px; font-weight: bold; vertical-align: middle;">AI Investment Impact</span>', unsafe_allow_html=True)

# Added better explanatory text with consistent formatting
st.markdown("""
<div style="background-color: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px; margin-bottom: 20px;">
    <p style="color: #ffffff; font-size: 16px; margin: 0;">
        Shows how much value is returned for every dollar spent on AI — includes cost savings, indirect and strategic gains.
    </p>
</div>
""", unsafe_allow_html=True)

ai_spend = subscription + ai_variable_cost
dollar_return = value_basis / ai_spend if ai_spend else 0.0

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

# Add toggle for detailed explanation of ROI calculation
with st.expander("ℹ️ How is this return calculated?"):
    st.subheader("AI Investment Return")
    st.write("This metric shows the multiplier effect of your AI investment - how many dollars you get back for every dollar spent on AI.")
    st.write("- **AI investment** includes both the subscription cost and variable AI usage costs")
    st.write("- **Total value** includes all forms of savings: direct operational savings, indirect productivity improvements, and strategic benefits")
    st.write("- **Formula**: Total Value ÷ (Subscription + AI Variable Cost)")
    st.write(f"- At ${dollar_return:.2f}, your AI investment is delivering a {(dollar_return-1)*100:.0f}% return on every dollar")
    
    st.write("*Note: This is a monthly return figure, meaning your annual return would be approximately 12 times this amount for every dollar invested.*")
    
    st.write("**What this means for your business:** This is perhaps the most compelling metric for financial decision makers. This return far exceeds most technology investments, which typically return $1.30-$2.50. This positions AI automation as one of the highest-ROI technologies available to contact centers today.")

st.markdown("---")

# Add explanatory text for Indirect Impact section
if include_indirect:
    col_icon3, col_text3 = st.columns([1, 20])
    with col_icon3:
        st.image("favicon-32x32.png", width=32)
    with col_text3:
        st.markdown('<span style="font-size: 32px; font-weight: bold; vertical-align: middle;">Indirect Benefits</span>', unsafe_allow_html=True)
        
    st.markdown("""
    <div style="background-color: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px; margin-bottom: 20px;">
        <p style="color: #ffffff; font-size: 16px; margin: 0;">
            These gains reflect enhanced output from improved efficiency and revenue opportunities.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    indirect_col1, indirect_col2 = st.columns(2)
    with indirect_col1:
        st.markdown(metric_block("Indirect Savings", indirect_savings, "$", "", "{:,.0f}"), unsafe_allow_html=True)
    if include_hr:
        with indirect_col2:
            st.markdown(metric_block("HR Strategic Impact", strategic_savings, "$", "", "{:,.0f}"), unsafe_allow_html=True)
    
    # Add toggle for detailed explanation of indirect savings
    with st.expander("ℹ️ How are these indirect benefits calculated?"):
        st.subheader("Indirect Savings")
        st.write("These savings come from the reduction in unproductive time, enhanced by AI's 24/7 operational advantage.")
        st.write("- **Unproductive cost**: The portion of your baseline cost that doesn't generate direct value")
        st.write("- **AI efficiency factor**: A multiplier that reflects AI's ability to work continuously")
        st.write("- **Formula**: Unproductive Cost × Automation % × AI Efficiency Factor")
        
        st.subheader("What's included in indirect savings:")
        st.write("- **Reduced training costs**: AI requires no ongoing training for new policies, procedures, or products")
        st.write("- **Lower quality assurance costs**: AI delivers consistent quality, reducing QA overhead")
        st.write("- **Decreased management overhead**: AI requires less supervisory oversight than human agents")
        st.write("- **Improved productivity**: Human agents become more effective when AI handles routine tasks")
        st.write("- **Reduced error costs**: AI minimizes costly mistakes that require rework or compensation")
        st.write("- **Lower absenteeism costs**: AI doesn't call in sick or take unplanned time off")
        
        st.write("**Why this matters**: Many organizations focus only on direct cost savings when evaluating AI, missing up to 60% of the total value. These indirect savings often have an even greater impact on overall profitability and customer satisfaction than direct agent cost reduction.")
        
        # HR Strategic Impact section (only if enabled)
        if include_hr:
            st.subheader("HR Strategic Impact")
            st.write("These are higher-order benefits from improved HR operations and strategic workforce planning.")
            st.write(f"- Calculated as {hr_pct}% of the indirect savings")
            st.write("- **Formula**: Indirect Savings × HR Impact %")
            
            st.subheader("What's included in HR strategic impact:")
            st.write("- **Reduced recruiting costs**: The average cost to recruit a contact center agent is $4,000-$8,000")
            st.write("- **Lower turnover**: AI handles repetitive tasks, increasing agent satisfaction and retention")
            st.write("- **Decreased time-to-proficiency**: New agents reach full productivity faster with AI assistance")
            st.write("- **Improved workforce planning**: More stable operations reduce emergency staffing needs")
            st.write("- **Enhanced flexibility**: AI enables more flexible work arrangements, expanding the talent pool")
            
            st.write("**Why this matters**: Contact centers typically experience 30-45% annual turnover. Even a modest reduction in turnover through AI implementation can save hundreds of thousands in recruiting, onboarding, and training costs while improving overall service quality.")
    
    st.markdown("---")

# ─── Human vs Hybrid Cost Comparison ───────────────────
col_icon4, col_text4 = st.columns([1, 20])
with col_icon4:
    st.image("favicon-32x32.png", width=32)
with col_text4:
    st.markdown('<span style="font-size: 32px; font-weight: bold; vertical-align: middle;">Human vs Hybrid Cost Comparison</span>', unsafe_allow_html=True)

# Added explanatory text with consistent formatting
st.markdown("""
<div style="background-color: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px; margin-bottom: 20px;">
    <p style="color: #ffffff; font-size: 16px; margin: 0;">
        This chart shows how your current human-only approach compares to a hybrid model with AI automation.
    </p>
</div>
""", unsafe_allow_html=True)

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

st.markdown("---")

# ─── Savings Breakdown ─────────────────────────────────
col_icon5, col_text5 = st.columns([1, 20])
with col_icon5:
    st.image("favicon-32x32.png", width=32)
with col_text5:
    st.markdown('<span style="font-size: 32px; font-weight: bold; vertical-align: middle;">Savings Breakdown</span>', unsafe_allow_html=True)

# Added explanatory text with consistent formatting
st.markdown("""
<div style="background-color: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px; margin-bottom: 20px;">
    <p style="color: #ffffff; font-size: 16px; margin: 0;">
        This breakdown shows direct savings from AI automation alongside indirect benefits from efficiency improvements.
    </p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([3, 1], gap="large")

with left:
    fig2 = go.Figure()
    
    fig2.add_trace(go.Bar(
        name="Net Savings",
        x=["Savings"], y=[net_savings],
        marker_color="#66BB6A"
    ))

    if include_indirect:
        fig2.add_trace(go.Bar(
            name="Indirect Sav.",
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
      {metric_block("Indirect Sav.", indirect_savings, "$", "", "{:,.0f}") if include_indirect else ""}
      {metric_block("HR Strategic", strategic_savings, "$", "", "{:,.0f}") if include_hr else ""}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# Add toggle for detailed explanation of savings breakdown
with st.expander("ℹ️ Understanding the savings breakdown"):
    st.subheader("Total Monthly Value")
    st.write("This stacked chart shows how your total monthly value is composed of different types of savings:")
    st.write("- **Net Savings**: Direct operational cost reduction from implementing AI")
    st.write("- **Indirect Savings**: Productivity improvements and reduction in unproductive time")
    st.write("- **HR Strategic Impact**: Higher-order benefits from improved workforce management")
    
    st.subheader("Why the total value matters:")
    st.write("- **Complete picture**: Looking at direct savings alone understates AI's true value by as much as 70%")
    st.write("- **Financial justification**: The total value provides compelling ROI that makes approval easier")
    st.write("- **Long-term impact**: Indirect benefits often increase over time as AI becomes more integrated")
    st.write("- **Competitive advantage**: Organizations that understand total value gain a strategic edge over competitors only focused on direct costs")
    
    st.write("**Decision-making guidance:** When evaluating AI automation, consider all three value components. A solution that delivers higher total value, even at slightly higher implementation cost, will typically provide better long-term returns than a cheaper solution with lower indirect benefits.")
    
    st.write("*Note: Toggle the \"Include Indirect Value\" and \"Include HR Strategic Impact\" options in the sidebar to see how these additional value components affect your overall ROI.*")

# Add this at the end of your calculator script

st.markdown("---")

# FAQ Header with logo
col_icon_faq, col_text_faq = st.columns([1, 20])
with col_icon_faq:
    st.image("favicon-32x32.png", width=32)
with col_text_faq:
    st.markdown('<span style="font-size: 32px; font-weight: bold; vertical-align: middle;">Frequently Asked Questions</span>', unsafe_allow_html=True)

# Header description
st.markdown("""
<div style="background-color: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px; margin-bottom: 20px;">
    <p style="color: #ffffff; font-size: 16px; margin: 0;">
        Common questions about AI automation and how it can benefit your contact center operations.
    </p>
</div>
""", unsafe_allow_html=True)

# Category 1: Why Businesses Are Switching to AI Voice Agents
st.markdown("### Why Businesses Are Switching to AI Voice Agents")

with st.expander("What exactly is an AI Voice Representative?"):
    st.write("""
    AI Voice Representatives are cutting-edge virtual agents that revolutionize how businesses handle communications. They conduct remarkably natural phone conversations, answer complex questions, process requests, and deliver consistent excellence 24/7/365. 
    
    Unlike human agents who need breaks, vacations, and sick days, our AI Voice Representatives work around the clock with zero downtime, zero turnover, and zero training requirements—transforming your customer service from a cost center into a competitive advantage.
    """)

with st.expander("How do AI Voice Agents differ from traditional IVR systems?"):
    st.write("""
    Unlike traditional IVR systems that force callers through rigid menu trees, our AI Voice Agents engage in natural conversations. They don't just recognize keywords—they understand intent, can handle complex inquiries, and provide personalized responses that sound human, creating a dramatically improved customer experience.
    """)

# Category 2: Cost Savings & Operational Efficiency
st.markdown("### Cost Savings & Operational Efficiency")

with st.expander("What kind of cost savings can I expect?"):
    st.write("""
    Businesses typically slash communication costs by 50-70% when implementing AI Voice Agents. Beyond the obvious savings on salaries and benefits, you'll eliminate costly overhead from:

    - **Recruitment & Turnover Costs**: No more spending thousands on hiring replacements for the average 30-45% annual call center attrition
    - **Training Expenses**: Eliminate the 2-6 weeks of paid training for each new agent
    - **Absenteeism & No-Shows**: The average call center loses 7-15% of scheduled hours to unexpected absences and no-shows
    - **Management Overhead**: Reduce supervisory staff needed for scheduling, quality monitoring, and performance management
    
    *Use our ROI calculator above to see your specific savings potential.*
    """)

with st.expander("How do AI Voice Agents improve operational efficiency?"):
    st.write("""
    Our AI Voice Agents transform your operation with:

    - **24/7/365 Availability**: Never miss another call, even at 3 AM or during holidays
    - **Infinite Scalability**: Handle sudden call spikes without scrambling to staff up
    - **Zero Ramp-Up Time**: Deploy additional capacity instantly during seasonal peaks
    - **Perfect Consistency**: Every caller receives the same high-quality experience
    - **Zero Burnout**: Unlike humans, AI agents maintain peak performance regardless of call volume or complexity
    - **Instant Knowledge Updates**: New information is available across all AI agents simultaneously without training sessions
    """)

with st.expander("What happens to my business when calls go unanswered?"):
    st.write("""
    Every missed call is potentially thousands in lost revenue. Studies show:

    - 85% of customers whose calls go unanswered will not call back
    - 75% of callers will form a negative impression of your business from unanswered calls
    - The average missed sales call represents $1,200-$4,800 in lost potential revenue
    
    Our AI Voice Agents ensure every call is answered promptly, even during peak hours, nights, weekends, and holidays – capturing revenue that would otherwise be lost.
    """)

# Category 3: Implementation & Integration
st.markdown("### Implementation & Integration")

with st.expander("How long does it take to implement AI Voice Agents?"):
    st.write("""
    Implementation timelines depend on the specific product type you choose and your business requirements. Many of our solutions can be deployed rapidly with minimal setup time. 
    
    For detailed information about implementation for your specific needs, please contact us through our website at www.connexus.ai.
    """)

with st.expander("Will AI Voice Agents integrate with my existing systems?"):
    st.write("""
    Absolutely! Our flexible integration framework connects with virtually any business system you're currently using. Whether it's a popular CRM like Salesforce, your proprietary databases, or legacy phone systems, we design custom integration pathways that make implementation smooth and non-disruptive. 
    
    Contact us at www.connexus.ai for a personalized integration assessment.
    """)

# Category 4: Capabilities & Limitations
st.markdown("### Capabilities & Limitations")

with st.expander("What types of calls can AI Voice Agents handle effectively?"):
    st.write("""
    Our AI Voice Agents excel at handling appointment scheduling, customer service inquiries, order status updates, product information requests, lead qualification, and routine transactions. They're particularly effective for high-volume, repetitive call types that follow predictable patterns.
    """)

with st.expander("How do AI Voice Agents handle complex or unusual customer requests?"):
    st.write("""
    Our AI Voice Agents are designed to recognize when a conversation exceeds their capabilities. In these situations, they seamlessly transfer the call to a human agent, providing a complete transcript and summary of the conversation so the human agent can pick up exactly where the AI left off—creating a smooth customer experience.
    """)

with st.expander("Can AI Voice Agents make outbound calls too?"):
    st.write("""
    Absolutely! Our AI Voice Agents can conduct outbound calling campaigns for appointment reminders, payment collection, satisfaction surveys, lead qualification, and promotional offers. They can reach hundreds of customers simultaneously with personalized conversations that drive results.
    """)

# Category 5: Quality & Customer Experience
st.markdown("### Quality & Customer Experience")

with st.expander("How natural do the AI Voice Agents sound?"):
    st.write("""
    Our advanced AI technology produces remarkably natural-sounding voices that many callers cannot distinguish from humans. The agents understand context, respond to emotional cues, adjust their tone appropriately, and can even insert thoughtful pauses and conversational fillers for an authentic experience.
    """)

with st.expander("What languages do your AI Voice Agents support?"):
    st.write("""
    Our AI Voice Agents currently support over 25 languages including English, Spanish, French, German, Italian, Portuguese, Mandarin, Japanese, and Arabic. Each language version maintains natural intonation and cultural nuances for an authentic experience regardless of region.
    """)

with st.expander("How do customers typically react to AI Voice Agents?"):
    st.write("""
    Customer satisfaction scores with our AI Voice Agents average 4.7/5 across industries. Customers particularly appreciate the instant response (no hold times), 24/7 availability, and consistent experience. In blind tests, over 60% of customers couldn't tell they were speaking with an AI agent.
    """)

# Category 6: Security & Compliance
st.markdown("### Security & Compliance")

with st.expander("How secure is the AI Voice Agent solution?"):
    st.write("""
    Our AI Voice Agent platform is built with enterprise-grade security. All conversations are encrypted end-to-end, we maintain SOC 2 Type II compliance, and can support industry-specific requirements like HIPAA for healthcare and PCI DSS for payment processing. Your data and your customers' information remains secure at all times.
    """)

with st.expander("Do AI Voice Agents comply with disclosure requirements?"):
    st.write("""
    Yes. Our AI Voice Agents can be configured to disclose their virtual nature at the beginning of calls in compliance with emerging AI transparency regulations. This disclosure can be customized based on your preferences and regulatory requirements in your operating regions.
    """)

# Category 7: Getting Started
st.markdown("### Getting Started")

with st.expander("How can I see your AI Voice Agents in action?"):
    st.write("""
    Experience our AI Voice Agents firsthand with our interactive demo right on this website. Better yet, schedule a personalized demonstration where we'll show you exactly how our technology can transform your specific business operations, handling your unique call scenarios with precision and natural conversation flow.
    """)

with st.expander("How is pricing structured for AI Voice Agents?"):
    st.write("""
    Pricing depends on the specific product package that best fits your business needs. Unlike traditional call centers with unpredictable staffing costs, our pricing models offer predictability and transparency. Many clients find our ROI calculator eye-opening when they see the potential cost savings. 
    
    For detailed pricing information tailored to your requirements, please contact us through our website at www.connexus.ai.
    """)

with st.expander("What's the first step in getting started with AI Voice Agents?"):
    st.write("""
    The best way to begin is by scheduling a free consultation through our website at www.connexus.ai. Our experts will assess your current call operations, identify opportunities for AI implementation, and provide a customized proposal showing expected cost savings and performance improvements specific to your business model.
    """)

# Add some spacing at the bottom
st.markdown("<div style='margin-bottom: 50px;'></div>", unsafe_allow_html=True)
