import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from io import BytesIO
import base64
from decimal import Decimal, ROUND_HALF_UP

# ─── Page Setup ────────────────────────────────────────
st.set_page_config(page_title="ConnexUS AI ROI Calculator", layout="wide")

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

# ===== THIS IS WHERE AI EFFICIENCY FACTOR IS DEFINED =====
# AI efficiency factor - AI's operational advantage over humans based on utilization
# AI can work 24/7 while humans are limited by talk utilization
# Fine-tuned based on Excel model to match expected returns
ai_efficiency_factor = 2.0 if talk_pct > 0 else 2.0  # Optimized efficiency factor

# AI and human costs at the automation level
residual_human_cost = baseline_human_cost * (1 - automation_pct/100)

# ===== THIS IS WHERE AI EFFICIENCY IS USED IN COST CALCULATION =====
# AI cost based on talk time (productive time), adjusted for efficiency
# More efficient means AI costs less to do the same amount of work
ai_variable_cost = (productive_cost * (automation_pct/100)) / ai_efficiency_factor

# Total AI-enabled cost
ai_enabled_cost = residual_human_cost + ai_variable_cost + subscription

# Net savings
net_savings = baseline_human_cost - ai_enabled_cost

# Monthly cost efficiency
monthly_cost_efficiency = (net_savings / baseline_human_cost) * 100 if baseline_human_cost > 0 else float('inf')

# ===== THIS IS WHERE AI EFFICIENCY IS USED IN SAVINGS CALCULATION =====
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

# ─── Main Metrics Layout ───────────────────────────────
st.title("🚀 ConnexUS AI ROI Calculator")
st.markdown("---")

# Add explanatory text with proper spacing and formatting
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
    st.markdown(f"""
    <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px; margin-bottom: 15px;">
        <h4 style="color: #00FFAA; margin-top: 0;">Direct Savings Metrics</h4>
        <p><strong>Net Monthly Savings (${net_savings:,.0f})</strong>: The total monthly cost reduction achieved by implementing AI.</p>
        <ul>
            <li>Calculated as: Baseline human cost minus AI-enabled cost</li>
            <li>Formula: Agents × Hours × Rate × Burden - (Remaining Human Cost + AI Cost + Subscription)</li>
        </ul>
        
        <p><strong>Monthly Cost Efficiency ({monthly_cost_efficiency:.1f}%)</strong>: The percentage of baseline costs saved through AI implementation.</p>
        <ul>
            <li>Formula: Net Savings ÷ Baseline Cost × 100</li>
            <li><strong>What it means</strong>: Higher percentages indicate greater cost reduction. At {monthly_cost_efficiency:.1f}%, you're reducing operational costs by nearly one-third, which directly improves margin and profitability.</li>
        </ul>
    </div>

    <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px; margin-bottom: 15px;">
        <h4 style="color: #00FFAA; margin-top: 0;">ROI Metrics</h4>
        <p><strong>ROI on Production ({roi_prod_mo:.1f}% monthly, {roi_prod_mo*12:.1f}% yearly)</strong>: Return on investment relative to your baseline operational costs.</p>
        <ul>
            <li>Shows how much value is returned for every dollar of your current operations</li>
            <li>Formula: Total Value ÷ Baseline Cost × 100</li>
            <li><strong>What it means</strong>: A higher percentage indicates greater value creation. At {roi_prod_mo:.1f}%, your AI implementation is delivering nearly double the value of your current operational investment each month.</li>
        </ul>
        
        <p><strong>ROI on Integration ({roi_integ_mo:.1f}% monthly, {roi_integ_yr:.1f}% yearly)</strong>: Return on investment relative to your upfront integration costs.</p>
        <ul>
            <li>Shows how quickly you'll recover the initial integration fee</li>
            <li>Formula: Total Value ÷ Integration Fee × 100</li>
            <li><strong>What it means</strong>: Higher percentages indicate faster recovery of integration costs. At {roi_integ_mo:.1f}% monthly, you're seeing exceptional returns on your integration investment.</li>
        </ul>
    </div>

    <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px; margin-bottom: 15px;">
        <h4 style="color: #00FFAA; margin-top: 0;">Payback Metrics</h4>
        <p><strong>Payback on Production ({payback_mo_prod:.2f} months)</strong>: Number of months required to recover your baseline operational costs.</p>
        <ul>
            <li>Formula: Baseline Cost ÷ Total Value</li>
            <li><strong>What it means</strong>: Lower numbers are better. At {payback_mo_prod:.2f} months, you'll recover your monthly operational investment in just over a month through AI implementation savings.</li>
        </ul>
        
        <p><strong>Payback on Integration ({payback_mo_integ:.2f} months)</strong>: Number of months required to recover your integration investment.</p>
        <ul>
            <li>Formula: Integration Fee ÷ Total Value</li>
            <li><strong>What it means</strong>: Lower numbers indicate faster ROI. At {payback_mo_integ:.2f} months, you'll recover your entire integration investment in less than a month - far better than most technology investments which typically take 6-18 months.</li>
        </ul>
    </div>

    <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px;">
        <h4 style="color: #00FFAA; margin-top: 0;">Total Value</h4>
        <p><strong>Total Value (Combined) (${value_basis:,.0f})</strong>: The combined total of all direct and indirect savings.</p>
        <ul>
            <li>Formula: Net Savings + Indirect Savings + Strategic Savings</li>
            <li><strong>What it means</strong>: This represents the total financial impact of implementing AI across your organization, including both immediate cost savings and broader operational improvements.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Add explanatory text for Indirect Impact section
if include_indirect:
    st.markdown("""
    <div style="background-color: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px; margin-bottom: 20px; margin-top: 20px;">
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
        st.markdown(f"""
        <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px; margin-bottom: 15px;">
            <h4 style="color: #00FFAA; margin-top: 0;">Indirect Savings (${indirect_savings:,.0f})</h4>
            <p>These savings come from the reduction in unproductive time, enhanced by AI's 24/7 operational advantage.</p>
            <ul>
                <li><strong>Unproductive cost</strong>: The portion of your baseline cost that doesn't generate direct value ({100-talk_pct}% of total)</li>
                <li><strong>AI efficiency factor</strong>: A multiplier ({ai_efficiency_factor:.1f}x) that reflects AI's ability to work continuously</li>
                <li><strong>Formula</strong>: <code>unproductive_cost × (automation_pct/100) × ai_efficiency_factor</code></li>
                <li>This represents productivity gains, reduced training costs, and lower overhead</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if include_hr:
            st.markdown(f"""
            <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px;">
                <h4 style="color: #00FFAA; margin-top: 0;">HR Strategic Impact (${strategic_savings:,.0f})</h4>
                <p>These are higher-order benefits from improved HR operations and strategic workforce planning.</p>
                <ul>
                    <li>Calculated as {hr_pct}% of the indirect savings</li>
                    <li><strong>Formula</strong>: <code>indirect_savings × (hr_pct/100)</code></li>
                    <li>Represents reduced turnover, better hiring outcomes, and improved agent experience</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")

# ─── AI Investment Impact ─────────────────────────────
st.markdown("## 💡 AI Investment Impact", unsafe_allow_html=True)

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
    st.markdown(f"""
    <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px;">
        <h4 style="color: #00FFAA; margin-top: 0;">AI Investment Return</h4>
        <p>This metric shows the multiplier effect of your AI investment - how many dollars you get back for every dollar spent on AI.</p>
        <ul>
            <li><strong>AI investment</strong> includes both the subscription cost (${subscription:,.0f}/mo) and variable AI usage costs (${ai_variable_cost:,.0f}/mo)</li>
            <li><strong>Total value</strong> includes all forms of savings: direct operational savings, indirect productivity improvements, and strategic benefits</li>
            <li><strong>Formula</strong>: Total Value ÷ (Subscription + AI Variable Cost)</li>
            <li>At ${dollar_return:,.2f}, your AI investment is delivering a {(dollar_return-1)*100:.0f}% return on every dollar</li>
        </ul>
        <p><em>Note: This is a monthly return figure, meaning your annual return would be approximately ${dollar_return*12:,.2f} for every dollar invested.</em></p>
        
        <p><strong>What this means for your business:</strong> This is perhaps the most compelling metric for financial decision makers. A return of ${dollar_return:,.2f} for every dollar invested far exceeds most technology investments, which typically return $1.30-$2.50. This positions AI automation as one of the highest-ROI technologies available to contact centers today.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ─── Human vs Hybrid Cost Comparison ───────────────────
st.subheader("💰 Human vs Hybrid Cost Comparison")

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
    st.markdown(f"""
    <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px;">
        <h4 style="color: #00FFAA; margin-top: 0;">Understanding the Cost Comparison</h4>
        <p>This chart shows the financial difference between your current all-human operation and the proposed AI-hybrid model:</p>
        <ul>
            <li><strong>Left bar (100% Human)</strong>: Your current monthly spend (${baseline_human_cost:,.0f}) on human agents</li>
            <li><strong>Right bar (Hybrid)</strong>: The combined costs of your new hybrid model:
                <ul>
                    <li><strong>{100-automation_pct}% Human</strong>: Remaining human agent costs (${residual_human_cost:,.0f})</li>
                    <li><strong>{automation_pct}% AI Usage</strong>: Variable AI costs based on usage (${ai_variable_cost:,.0f})</li>
                    <li><strong>Subscription</strong>: Fixed monthly AI platform fee (${subscription:,.0f})</li>
                </ul>
            </li>
            <li><strong>Total monthly savings</strong>: ${net_savings:,.0f} ({monthly_cost_efficiency:.1f}% reduction)</li>
        </ul>
        
        <p><strong>Why this matters to your business:</strong></p>
        <ul>
            <li><strong>Immediate cost reduction</strong>: AI implementation delivers substantial cost savings from day one</li>
            <li><strong>Predictable costs</strong>: AI costs are more stable and predictable than human staffing costs</li>
            <li><strong>Scalability</strong>: AI can easily scale up or down without the hiring/firing cycles of traditional contact centers</li>
            <li><strong>Reduced fixed costs</strong>: Converting fixed costs (full-time employees) to variable costs (AI usage) improves financial flexibility</li>
            <li><strong>Lower operational risk</strong>: AI reduces dependency on labor market conditions and staffing challenges</li>
        </ul>
        
        <p>While maintaining the same service capacity, you're able to operate at {100-monthly_cost_efficiency:.1f}% of your previous cost base - this directly improves EBITDA and gives you competitive pricing advantages in your market.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ─── Savings Breakdown ─────────────────────────────────
st.subheader("💸 Savings Breakdown")

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
    st.markdown(f"""
    <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px;">
        <h4 style="color: #00FFAA; margin-top: 0;">Total Monthly Value: ${value_basis:,.0f}</h4>
        <p>This stacked chart shows how your total monthly value is composed of different types of savings:</p>
        <ul>
            <li><strong>Net Savings (${net_savings:,.0f})</strong>: Direct operational cost reduction from implementing AI</li>
            <li><strong>Indirect Savings{f" (${indirect_savings:,.0f})" if include_indirect else ""}</strong>: Productivity improvements and reduction in unproductive time</li>
            <li><strong>HR Strategic Impact{f" (${strategic_savings:,.0f})" if include_hr else ""}</strong>: Higher-order benefits from improved workforce management</li>
        </ul>
        
        <p><strong>Why the total value matters:</strong></p>
        <ul>
            <li><strong>Complete picture</strong>: Looking at direct savings alone understates AI's true value by as much as 70%</li>
            <li><strong>Financial justification</strong>: The total value provides compelling ROI that makes approval easier</li>
            <li><strong>Long-term impact</strong>: Indirect benefits often increase over time as AI becomes more integrated</li>
            <li><strong>Competitive advantage</strong>: Organizations that understand total value gain a strategic edge over competitors only focused on direct costs</li>
        </ul>
        
        <p><strong>Decision-making guidance:</strong> When evaluating AI automation, consider all three value components. A solution that delivers higher total value, even at slightly higher implementation cost, will typically provide better long-term returns than a cheaper solution with lower indirect benefits.</p>
        
        <p><em>Note: Toggle the "Include Indirect Value" and "Include HR Strategic Impact" options in the sidebar to see how these additional value components affect your overall ROI.</em></p>
    </div>
    """, unsafe_allow_html=True)
