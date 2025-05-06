# Main metrics expander
with st.expander("ℹ️ How are these metrics calculated?"):
    st.markdown("""
    <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px; margin-bottom: 15px;">
        <h4 style="color: #00FFAA; margin-top: 0;">Direct Savings Metrics</h4>
        <p><strong>Net Monthly Savings</strong>: The total monthly cost reduction achieved by implementing AI.</p>
        <ul>
            <li>Calculated as: Baseline human cost minus AI-enabled cost</li>
            <li>Formula: Agents × Hours × Rate × Burden - (Remaining Human Cost + AI Cost + Subscription)</li>
        </ul>
        
        <p><strong>Monthly Cost Efficiency</strong>: The percentage of baseline costs saved through AI implementation.</p>
        <ul>
            <li>Formula: Net Savings ÷ Baseline Cost × 100</li>
            <li><strong>What it means</strong>: Higher percentages indicate greater cost reduction. This directly improves margin and profitability.</li>
        </ul>
    </div>

    <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px; margin-bottom: 15px;">
        <h4 style="color: #00FFAA; margin-top: 0;">ROI Metrics</h4>
        <p><strong>ROI on Production</strong>: Return on investment relative to your baseline operational costs.</p>
        <ul>
            <li>Shows how much value is returned for every dollar of your current operations</li>
            <li>Formula: Total Value ÷ Baseline Cost × 100</li>
            <li><strong>What it means</strong>: A higher percentage indicates greater value creation. Your AI implementation is delivering nearly double the value of your current operational investment each month.</li>
        </ul>
        
        <p><strong>ROI on Integration</strong>: Return on investment relative to your upfront integration costs.</p>
        <ul>
            <li>Shows how quickly you'll recover the initial integration fee</li>
            <li>Formula: Total Value ÷ Integration Fee × 100</li>
            <li><strong>What it means</strong>: Higher percentages indicate faster recovery of integration costs. You're seeing exceptional returns on your integration investment.</li>
        </ul>
    </div>

    <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px; margin-bottom: 15px;">
        <h4 style="color: #00FFAA; margin-top: 0;">Payback Metrics</h4>
        <p><strong>Payback on Production</strong>: Number of months required to recover your baseline operational costs.</p>
        <ul>
            <li>Formula: Baseline Cost ÷ Total Value</li>
            <li><strong>What it means</strong>: Lower numbers are better. You'll recover your monthly operational investment quickly through AI implementation savings.</li>
        </ul>
        
        <p><strong>Payback on Integration</strong>: Number of months required to recover your integration investment.</p>
        <ul>
            <li>Formula: Integration Fee ÷ Total Value</li>
            <li><strong>What it means</strong>: Lower numbers indicate faster ROI. You'll recover your entire integration investment in less than a month - far better than most technology investments which typically take 6-18 months.</li>
        </ul>
    </div>

    <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px;">
        <h4 style="color: #00FFAA; margin-top: 0;">Total Value</h4>
        <p><strong>Total Value (Combined)</strong>: The combined total of all direct and indirect savings.</p>
        <ul>
            <li>Formula: Net Savings + Indirect Savings + Strategic Savings</li>
            <li><strong>What it means</strong>: This represents the total financial impact of implementing AI across your organization, including both immediate cost savings and broader operational improvements.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# AI Investment Return expander
with st.expander("ℹ️ How is this return calculated?"):
    st.markdown("""
    <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px;">
        <h4 style="color: #00FFAA; margin-top: 0;">AI Investment Return</h4>
        <p>This metric shows the multiplier effect of your AI investment - how many dollars you get back for every dollar spent on AI.</p>
        <ul>
            <li><strong>AI investment</strong> includes both the subscription cost and variable AI usage costs</li>
            <li><strong>Total value</strong> includes all forms of savings: direct operational savings, indirect productivity improvements, and strategic benefits</li>
            <li><strong>Formula</strong>: Total Value ÷ (Subscription + AI Variable Cost)</li>
            <li>Your AI investment is delivering a significant return on every dollar</li>
        </ul>
        <p><em>Note: This is a monthly return figure, meaning your annual return would be approximately 12 times this amount for every dollar invested.</em></p>
        
        <p><strong>What this means for your business:</strong> This is perhaps the most compelling metric for financial decision makers. This return far exceeds most technology investments, which typically return $1.30-$2.50. This positions AI automation as one of the highest-ROI technologies available to contact centers today.</p>
    </div>
    """, unsafe_allow_html=True)

# Indirect benefits expander
with st.expander("ℹ️ How are these indirect benefits calculated?"):
    st.markdown("""
    <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px; margin-bottom: 15px;">
        <h4 style="color: #00FFAA; margin-top: 0;">Indirect Savings</h4>
        <p>These savings come from the reduction in unproductive time, enhanced by AI's 24/7 operational advantage.</p>
        <ul>
            <li><strong>Unproductive cost</strong>: The portion of your baseline cost that doesn't generate direct value</li>
            <li><strong>AI efficiency factor</strong>: A multiplier that reflects AI's ability to work continuously</li>
            <li><strong>Formula</strong>: Unproductive Cost × Automation % × AI Efficiency Factor</li>
        </ul>
        
        <p><strong>What's included in indirect savings:</strong></p>
        <ul>
            <li><strong>Reduced training costs</strong>: AI requires no ongoing training for new policies, procedures, or products</li>
            <li><strong>Lower quality assurance costs</strong>: AI delivers consistent quality, reducing QA overhead</li>
            <li><strong>Decreased management overhead</strong>: AI requires less supervisory oversight than human agents</li>
            <li><strong>Improved productivity</strong>: Human agents become more effective when AI handles routine tasks</li>
            <li><strong>Reduced error costs</strong>: AI minimizes costly mistakes that require rework or compensation</li>
            <li><strong>Lower absenteeism costs</strong>: AI doesn't call in sick or take unplanned time off</li>
        </ul>
        
        <p><strong>Why this matters</strong>: Many organizations focus only on direct cost savings when evaluating AI, missing up to 60% of the total value. These indirect savings often have an even greater impact on overall profitability and customer satisfaction than direct agent cost reduction.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # HR Strategic Impact section (only if enabled)
    if include_hr:
        st.markdown("""
        <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px;">
            <h4 style="color: #00FFAA; margin-top: 0;">HR Strategic Impact</h4>
            <p>These are higher-order benefits from improved HR operations and strategic workforce planning.</p>
            <ul>
                <li>Calculated as a percentage of the indirect savings</li>
                <li><strong>Formula</strong>: Indirect Savings × HR Impact %</li>
            </ul>
            
            <p><strong>What's included in HR strategic impact:</strong></p>
            <ul>
                <li><strong>Reduced recruiting costs</strong>: The average cost to recruit a contact center agent is $4,000-$8,000</li>
                <li><strong>Lower turnover</strong>: AI handles repetitive tasks, increasing agent satisfaction and retention</li>
                <li><strong>Decreased time-to-proficiency</strong>: New agents reach full productivity faster with AI assistance</li>
                <li><strong>Improved workforce planning</strong>: More stable operations reduce emergency staffing needs</li>
                <li><strong>Enhanced flexibility</strong>: AI enables more flexible work arrangements, expanding the talent pool</li>
            </ul>
            
            <p><strong>Why this matters</strong>: Contact centers typically experience 30-45% annual turnover. Even a modest reduction in turnover through AI implementation can save hundreds of thousands in recruiting, onboarding, and training costs while improving overall service quality.</p>
        </div>
        """, unsafe_allow_html=True)

# Cost comparison expander
with st.expander("ℹ️ How to read this cost comparison"):
    st.markdown("""
    <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px;">
        <h4 style="color: #00FFAA; margin-top: 0;">Understanding the Cost Comparison</h4>
        <p>This chart shows the financial difference between your current all-human operation and the proposed AI-hybrid model:</p>
        <ul>
            <li><strong>Left bar (100% Human)</strong>: Your current monthly spend on human agents</li>
            <li><strong>Right bar (Hybrid)</strong>: The combined costs of your new hybrid model:
                <ul>
                    <li><strong>Remaining Human</strong>: Remaining human agent costs</li>
                    <li><strong>AI Usage</strong>: Variable AI costs based on usage</li>
                    <li><strong>Subscription</strong>: Fixed monthly AI platform fee</li>
                </ul>
            </li>
        </ul>
        
        <p><strong>Why this matters to your business:</strong></p>
        <ul>
            <li><strong>Immediate cost reduction</strong>: AI implementation delivers substantial cost savings from day one</li>
            <li><strong>Predictable costs</strong>: AI costs are more stable and predictable than human staffing costs</li>
            <li><strong>Scalability</strong>: AI can easily scale up or down without the hiring/firing cycles of traditional contact centers</li>
            <li><strong>Reduced fixed costs</strong>: Converting fixed costs (full-time employees) to variable costs (AI usage) improves financial flexibility</li>
            <li><strong>Lower operational risk</strong>: AI reduces dependency on labor market conditions and staffing challenges</li>
        </ul>
        
        <p>While maintaining the same service capacity, you're able to operate at a significantly lower cost base - this directly improves EBITDA and gives you competitive pricing advantages in your market.</p>
    </div>
    """, unsafe_allow_html=True)

# Savings breakdown expander
with st.expander("ℹ️ Understanding the savings breakdown"):
    st.markdown("""
    <div style="background-color: rgba(0,0,0,0.1); padding: 15px; border-radius: 5px;">
        <h4 style="color: #00FFAA; margin-top: 0;">Total Monthly Value</h4>
        <p>This stacked chart shows how your total monthly value is composed of different types of savings:</p>
        <ul>
            <li><strong>Net Savings</strong>: Direct operational cost reduction from implementing AI</li>
            <li><strong>Indirect Savings</strong>: Productivity improvements and reduction in unproductive time</li>
            <li><strong>HR Strategic Impact</strong>: Higher-order benefits from improved workforce management</li>
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
