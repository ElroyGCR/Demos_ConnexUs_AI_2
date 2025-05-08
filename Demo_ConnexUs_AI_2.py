import streamlit as st
import plotly.graph_objects as go
from PIL import Image
import os
from decimal import Decimal, ROUND_HALF_UP

# ─── Page Setup ────────────────────────────────────────
st.set_page_config(page_title="ConnexUS AI ROI Calculator", layout="wide")

# Add space at the top with native Streamlit
for _ in range(3):
    st.write("")

# ─── Logo Display - Native Streamlit ─────────────────────
# Try to load and display logo with native Streamlit components
try:
    logo_path = "connexus_logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=200)
    else:
        st.title("ConnexUS")
except Exception:
    st.title("ConnexUS")

# Add a little space after logo
st.write("")

# ─── Helpers ───────────────────────────────────────────
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

# ─── ROI Metrics & Investment Impact Section ──────────────────────────
st.header("ROI Metrics & Investment Impact")

st.write("These key metrics show your cost savings and the value returned for every dollar invested in AI automation.")

# Create a layout for metric display using columns
col1, col2, col3 = st.columns(3)

# Display metrics using native Streamlit components
with col1:
    st.metric("Direct Monthly Savings", f"${int(direct_savings):,}")
    
with col2:
    st.metric("Total Value (Combined savings)", f"${int(value_basis):,}")
    
with col3:
    st.metric("Monthly Cost Efficiency", f"{monthly_cost_efficiency:.1f}%")

# Add spacing
st.write("")

# Second row of metrics
row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.metric("ROI on Integration (yr)", f"{roi_integ_yr:.1f}%")
    
with row2_col2:
    st.metric("Payback on Int (months)", f"{payback_mo_integ:.2f}")

# AI Investment Return Display using native components
ai_spend = subscription + ai_variable_cost
dollar_return = value_basis / ai_spend if ai_spend else 0.0

# Add spacing
st.write("")

# Display the key metric in a prominent way
st.subheader(f"For every $1 you invest in AI, you save: ${dollar_return:.2f}")

# Explanation expander
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
st.header("Human vs Hybrid Cost Comparison")

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
st.header("Savings Breakdown")

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
    # Use native Streamlit metrics for the right column
    st.metric("Direct Savings", f"${int(direct_savings):,}")
    if include_indirect:
        st.metric("Indirect Savings", f"${int(indirect_savings):,}")
    if include_hr:
        st.metric("HR Strategic", f"${int(strategic_savings):,}")

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

# ─── Frequently Asked Questions ────────────────────
st.header("Frequently Asked Questions")

# Simple text description 
st.write("Common questions about AI automation and how it can benefit your contact center operations.")

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
    st.subheader("Why Businesses Are Switching to AI Voice Agents")
    
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
    st.subheader("Cost Savings & Operational Efficiency")
    
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
    st.subheader("Implementation & Integration")
    
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
    st.subheader("Capabilities & Customer Experience")
    
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
    st.subheader("Getting Started & Pricing")
    
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
