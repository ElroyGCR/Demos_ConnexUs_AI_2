# ─── Main Title ─────────────────────────────────────────
st.title("ConnexUS AI ROI Calculator")
st.markdown("---")

# ─── Combined Metrics Overview and AI Investment Impact Section ──────────────────────────
col_icon1, col_text1 = st.columns([1, 20])
with col_icon1:
    st.image("favicon-32x32.png", width=32)
with col_text1:
    st.markdown('<span style="font-size: 32px; font-weight: bold; vertical-align: middle;">ROI Metrics & Investment Impact</span>', unsafe_allow_html=True)

st.markdown("""
<div style="background-color: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px; margin-bottom: 20px;">
    <p style="color: #ffffff; font-size: 16px; margin: 0;">
        These key metrics show your cost savings and the value returned for every dollar invested in AI automation.
    </p>
</div>
""", unsafe_allow_html=True)

# First row - 3 metrics
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(metric_block("Direct Monthly Savings", direct_savings, "$", "", "{:,.0f}"), unsafe_allow_html=True)
with c2:
    st.markdown(metric_block("Total Value (Combined savings)", value_basis, "$", "", "{:,.0f}"), unsafe_allow_html=True)
with c3:
    st.markdown(metric_block("Monthly Cost Efficiency", monthly_cost_efficiency, "", "%", "{:,.1f}"), unsafe_allow_html=True)

# Add spacing between the rows of metric cards
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

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
    padding: 20px 30px;
    margin-top: 20px;
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

st.markdown("---")
