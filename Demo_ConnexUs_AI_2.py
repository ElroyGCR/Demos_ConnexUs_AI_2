# Streamlit AI Savings Calculator
# -----------------------------------
# This script requires Streamlit. Make sure you have it installed in your environment:
#     pip install streamlit

import sys
import os
import math

# Attempt to import Streamlit and other required libraries
try:
    import streamlit as st
    import plotly.graph_objects as go
    import plotly.express as px
    import pandas as pd
    import numpy as np
except ImportError as e:
    sys.exit(
        f"Error: Required module not found: {e.name}\n"
        f"Please install it by running 'pip install {e.name}' in your environment."
    )

# ─── Page Setup ────────────────────────────────────────
# IMPORTANT: st.set_page_config must be the first Streamlit command
st.set_page_config(page_title="AI Savings Calculator", layout="wide", page_icon="💰")

# ─── Calculation Logic ─────────────────────────────────
def calculate_metrics(
    agents: int,
    human_rate: float,
    burden_pct: float,
    talk_pct: float,
    hours_per_month: float,
    subscription: float,
    automation_pct: float,
    integration_fee: float,
    include_indirect: bool,
    hr_pct: float,
    ai_efficiency_factor: float = 2.0
) -> dict:
    """
    Compute AI savings metrics based on inputs.
    Returns a dict with keys for all core metrics.
    """
    burden_mul = 1 + burden_pct / 100
    baseline = agents * hours_per_month * human_rate * burden_mul
    productive = baseline * (talk_pct / 100)
    unproductive = baseline * (1 - talk_pct / 100)
    residual = baseline * (1 - automation_pct / 100)
    ai_variable = (productive * (automation_pct / 100)) / ai_efficiency_factor
    ai_enabled = residual + ai_variable + subscription
    net_savings = baseline - ai_enabled
    monthly_eff = (net_savings / baseline) * 100 if baseline > 0 else float('nan')
    indirect = unproductive * (automation_pct / 100) * ai_efficiency_factor if include_indirect else 0.0
    strategic = indirect * (hr_pct / 100) if include_indirect else 0.0
    total_value = net_savings + indirect + strategic
    roi_integ_mo = (total_value / integration_fee) * 100 if integration_fee > 0 else float('nan')
    roi_integ_yr = roi_integ_mo * 12 if math.isfinite(roi_integ_mo) else float('nan')
    payback_integ = integration_fee / total_value if total_value > 0 else float('nan')
    roi_prod_mo = (total_value / baseline) * 100 if baseline > 0 else float('nan')
    payback_prod = baseline / total_value if total_value > 0 else float('nan')
    ai_spend = subscription + ai_variable
    return_per = total_value / ai_spend if ai_spend > 0 else float('nan')

    return {
        'burden_mul': burden_mul,
        'baseline_human_cost': baseline,
        'productive_cost': productive,
        'unproductive_cost': unproductive,
        'residual_human_cost': residual,
        'ai_variable_cost': ai_variable,
        'ai_enabled_cost': ai_enabled,
        'net_savings': net_savings,
        'monthly_cost_efficiency': monthly_eff,
        'indirect_savings': indirect,
        'strategic_savings': strategic,
        'total_value': total_value,
        'roi_integ_mo': roi_integ_mo,
        'roi_integ_yr': roi_integ_yr,
        'payback_mo_integ': payback_integ,
        'roi_prod_mo': roi_prod_mo,
        'payback_mo_prod': payback_prod,
        'ai_spend': ai_spend,
        'return_per_dollar': return_per,
    }

# ─── Styles ────────────────────────────────────────────
st.markdown("""
<style>
  .banner { background-color: #E0F7FA; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
  .result-card { background-color: #F1F8E9; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
  .tooltip { cursor: help; color: #0288D1; margin-left: 5px; }
  .stApp {
    background-color: #0f1116;
    color: #ffffff;
  }
  .css-145kmo2 {
    color: #ffffff;
  }
</style>
""", unsafe_allow_html=True)

# ─── Main App Layout ─────────────────────────────────────
st.title("AI Savings Calculator")

# Example Story 
st.markdown("""
> **Meet Alex.** Alex has 10 people who each work 160 hours a month at $20/hour. By letting AI help with 40% of the work,
> Alex keeps an extra $8,000 each month and gets the $10,000 setup fee back in just 3 months!
""")
st.markdown("---")

# Create two columns for layout
input_col, graph_col = st.columns([1, 2])

# ─── Input Panel (Left Column) ─────────────────────────────
with input_col:
    st.header("Your Information")
    agents = st.number_input("Number of People", min_value=1, value=10, step=1)
    human_rate = st.number_input("Pay Per Hour", min_value=1.0, value=20.0, step=1.0)
    burden_pct = st.slider("Extra Cost for Benefits (%)", 0, 100, 30, step=5)
    hours_per_month = st.number_input("Hours Worked Each Month", min_value=1.0, value=160.0, step=1.0)
    talk_pct = st.slider("Percent of Time Helping Customers", 0, 100, 50, step=5)

    st.subheader("AI Costs")
    subscription = st.number_input("Monthly AI Fee ($)", min_value=0.0, value=1000.0, step=50.0)
    ai_cost_min = st.number_input("AI Talk Cost (per min)", min_value=0.01, value=0.20, step=0.01)
    automation_pct = st.slider("Goal: How Much AI Will Help (%)", 0, 100, 40, step=5)
    integration_fee = st.number_input("One-Time Setup Cost ($)", min_value=0.0, value=10000.0, step=500.0)

    include_indirect = st.checkbox("Include Extra Savings (fewer mistakes, happier staff)", value=True)
    hr_pct = st.slider("Extra Savings: What percent to count?", 0, 100, 10, step=5) if include_indirect else 0

# ─── Results and Graphs (Right Column) ─────────────────────
with graph_col:
    # Calculate metrics with try/except block to catch any calculation errors
    try:
        metrics = calculate_metrics(
            agents=agents,
            human_rate=human_rate,
            burden_pct=burden_pct,
            talk_pct=talk_pct,
            hours_per_month=hours_per_month,
            subscription=subscription,
            automation_pct=automation_pct,
            integration_fee=integration_fee,
            include_indirect=include_indirect,
            hr_pct=hr_pct,
        )
    except Exception as e:
        st.error(f"Error calculating metrics: {str(e)}")
        # Create an empty metrics dictionary to prevent downstream errors
        metrics = {}
    
    # Display the main banner
    try:
        net = metrics.get('net_savings', 0)
        ret = metrics.get('return_per_dollar', 0)
        payback = metrics.get('payback_mo_integ', 0)
        
        # Format the values carefully to avoid f-string confusion
        if math.isfinite(net) and net is not None:
            banner_net = f"${int(net):,}"
        else:
            banner_net = "$0"
            
        banner_ret = f"{ret:,.2f}" if math.isfinite(ret) and ret is not None else "0.00"
        banner_pay = f"{payback:.1f}" if math.isfinite(payback) and payback is not None else "N/A"

        st.markdown(f"""
        <div class='banner'>
          <h2>You'll save <span style='color:#2E7D32;'>{banner_net}</span> each month!</h2>
          <p>For every $1 you spend on AI, you get {banner_ret} back.</p>
          <p>You'll get your setup money back in {banner_pay} months.</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error displaying banner: {str(e)}")
        # Show a simpler banner as fallback
        st.markdown("""
        <div class='banner'>
          <h2>Calculate your AI savings above</h2>
          <p>Adjust the values on the left to see your potential savings.</p>
        </div>
        """, unsafe_allow_html=True)

    # ─── GRAPH 1: Cost Comparison Bar Chart ─────────────────
    st.subheader("Monthly Cost Comparison")
    
    try:
        baseline_cost = metrics.get('baseline_human_cost', 0)
        ai_enabled_cost = metrics.get('ai_enabled_cost', 0)
        net_savings = metrics.get('net_savings', 0)
        
        fig_cost = go.Figure()
        fig_cost.add_trace(go.Bar(
            x=['Current Human Cost', 'AI-Enabled Cost', 'Net Savings'],
            y=[baseline_cost, ai_enabled_cost, net_savings],
            marker_color=['#ff9e80', '#80cbc4', '#2E7D32']
        ))
        fig_cost.update_layout(
            xaxis_title="Cost Category",
            yaxis_title="Amount ($)",
            yaxis_tickprefix="$",
            plot_bgcolor='rgba(0,0,0,0.1)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=300,
            margin=dict(l=40, r=40, t=30, b=40),
        )
        st.plotly_chart(fig_cost, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not display Cost Comparison chart: {str(e)}")
    
    # ─── GRAPH 2: ROI Timeline Graph ─────────────────
    st.subheader("Return on Investment Over Time")
    
    try:
        # Generate timeline data for 24 months
        months = list(range(1, 25))
        
        # Calculate cumulative savings - handle missing values safely
        monthly_value = metrics.get('total_value', 0)
        
        # Check if integration_fee exists and is valid
        if 'integration_fee' in metrics and isinstance(metrics['integration_fee'], (int, float)):
            initial_investment = float(metrics['integration_fee'])
        else:
            # Use a default or the value from input if metrics doesn't have it
            initial_investment = integration_fee
            
        # Start with negative investment
        cumulative = []
        for i in range(len(months)):
            # For month i, we have the initial negative investment plus i months of positive value
            cumulative.append(-initial_investment + (monthly_value * (i+1)))
        
        # Create dataframe for the line chart
        roi_data = pd.DataFrame({
            'Month': months,
            'Cumulative Value': cumulative
        })
        
        # Find break-even point - the first month where cumulative value becomes positive
        breakeven_month = next((i for i, val in enumerate(cumulative) if val >= 0), None)
        
        # Create the ROI timeline chart
        fig_roi = px.line(
            roi_data, 
            x='Month', 
            y='Cumulative Value',
            markers=True,
        )
        
        # Add break-even point marker if we found one
        if breakeven_month is not None:
            fig_roi.add_trace(
                go.Scatter(
                    x=[months[breakeven_month]], 
                    y=[cumulative[breakeven_month]],
                    mode='markers',
                    marker=dict(size=12, color='#76ff03', line=dict(width=2, color='white')),
                    name='Break-even Point'
                )
            )
        
        # Add horizontal line at y=0
        fig_roi.add_shape(
            type="line", line_color="gray", line_dash="dash",
            x0=0, x1=24, y0=0, y1=0
        )
        
        fig_roi.update_layout(
            xaxis_title="Month",
            yaxis_title="Cumulative Value ($)",
            yaxis_tickprefix="$",
            plot_bgcolor='rgba(0,0,0,0.1)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=300,
            margin=dict(l=40, r=40, t=30, b=40),
        )
        st.plotly_chart(fig_roi, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not display ROI Timeline chart: {str(e)}")
        
    # Create two columns for smaller charts
    col1, col2 = st.columns(2)
    
    # ─── GRAPH 3: Cost Breakdown Pie Charts ─────────────────
    with col1:
        st.subheader("Cost Distribution")
        
        try:
            # Safely extract data for the pie charts with fallbacks
            residual_human_cost = metrics.get('residual_human_cost', 0)
            productive_cost = metrics.get('productive_cost', 0)
            unproductive_cost = metrics.get('unproductive_cost', 0)
            ai_variable_cost = metrics.get('ai_variable_cost', 0)
            subscription_cost = subscription  # Use the direct input value
            
            # Calculate replaced cost
            replaced_cost = productive_cost * (automation_pct / 100) if productive_cost else 0
            
            # Create tabs for the pie charts
            tab1, tab2 = st.tabs(["Before AI", "After AI"])
            
            with tab1:
                # Handle empty or invalid data
                if productive_cost <= 0 and unproductive_cost <= 0:
                    st.info("Not enough data to display the cost distribution chart.")
                else:
                    fig_pie1 = go.Figure(data=[go.Pie(
                        labels=['Human Productive', 'Human Unproductive'],
                        values=[productive_cost, unproductive_cost],
                        hole=.4,
                        marker_colors=['#ff9e80', '#ffcc80']
                    )])
                    fig_pie1.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=300,
                        margin=dict(l=20, r=20, t=30, b=20),
                    )
                    st.plotly_chart(fig_pie1, use_container_width=True)
                
            with tab2:
                # Handle empty or invalid data
                if residual_human_cost <= 0 and ai_variable_cost <= 0 and subscription_cost <= 0:
                    st.info("Not enough data to display the AI cost distribution chart.")
                else:
                    fig_pie2 = go.Figure(data=[go.Pie(
                        labels=['Remaining Human', 'AI Variable', 'AI Subscription'],
                        values=[residual_human_cost, ai_variable_cost, subscription_cost],
                        hole=.4,
                        marker_colors=['#ff9e80', '#80cbc4', '#4db6ac']
                    )])
                    fig_pie2.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        height=300,
                        margin=dict(l=20, r=20, t=30, b=20),
                    )
                    st.plotly_chart(fig_pie2, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not display Cost Distribution charts: {str(e)}")
    
    # ─── GRAPH 4: Value Component Waterfall Chart ─────────────────
    with col2:
        st.subheader("Total Value Breakdown")
        
        try:
            # Safely extract values
            net_savings = metrics.get('net_savings', 0)
            indirect_savings = metrics.get('indirect_savings', 0)
            strategic_savings = metrics.get('strategic_savings', 0)
            
            # Prepare waterfall chart data
            waterfall_x = ['Net Savings', 'Indirect Savings', 'Strategic Value', 'Total Value']
            waterfall_y = [
                net_savings, 
                indirect_savings, 
                strategic_savings, 
                0  # This is a dummy value for the total
            ]
            
            # Create waterfall chart
            fig_waterfall = go.Figure(go.Waterfall(
                name="Value Sources", 
                orientation="v",
                measure=["relative", "relative", "relative", "total"],
                x=waterfall_x,
                y=waterfall_y,
                connector={"line":{"color":"rgb(63, 63, 63)"}},
                decreasing={"marker":{"color":"#ff9e80"}},
                increasing={"marker":{"color":"#4db6ac"}},
                totals={"marker":{"color":"#76ff03"}},
            ))
            
            fig_waterfall.update_layout(
                title="",
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0.1)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=300,
                margin=dict(l=20, r=20, t=30, b=40),
                yaxis_tickprefix="$",
            )
            st.plotly_chart(fig_waterfall, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not display Value Breakdown chart: {str(e)}")

# ─── Unit Tests ─────────────────────────────────────
if not os.getenv('STREAMLIT_RUN'):
    def _almost_equal(a, b, tol=1e-6): return abs((a or 0) - (b or 0)) < tol
    test_inputs = dict(
        agents=10,
        human_rate=20.0,
        burden_pct=30,
        talk_pct=50,
        hours_per_month=160.0,
        subscription=1000.0,
        automation_pct=40,
        integration_fee=10000.0,
        include_indirect=True,
        hr_pct=10,
    )
    expected = calculate_metrics(**test_inputs)
    got = calculate_metrics(**test_inputs)
    assert set(got.keys()) == set(expected.keys()), "Mismatch in metric keys"
    for k in expected:
        assert _almost_equal(got[k], expected[k]), f"Metric {k} - expected {expected[k]}, got {got[k]}"
    print("All unit tests passed!")
