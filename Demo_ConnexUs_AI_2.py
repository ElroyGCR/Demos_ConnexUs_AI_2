# Replace the entire FAQ section with this ultra-simplified version

# ─── FAQ Section - Ultra Simplified ────────────────────
st.markdown("<h2 style='color: white; margin-bottom: 0.5rem;'>Frequently Asked Questions</h2>", unsafe_allow_html=True)

# Header description with larger font size
st.markdown("""
<div style="background-color: rgba(0,0,0,0.2); padding: 12px; border-radius: 5px; margin-bottom: 15px;">
    <p style="color: #ffffff; font-size: 20px; margin: 0; font-weight: 500;">
        Common questions about AI automation and how it can benefit your contact center operations.
    </p>
</div>
""", unsafe_allow_html=True)

# Ultra-simple approach: Just use a Markdown link that looks like a button
st.markdown("""
<div style="text-align: center; margin-bottom: 30px;">
    <a href="https://www.connexus.ai/faqs" target="_blank" style="
        background-color: rgba(0,0,0,0.3);
        color: #00FFAA;
        font-size: 18px;
        font-weight: 600;
        text-decoration: none;
        padding: 12px 24px;
        border-radius: 6px;
        border: 2px solid #00FFAA;
        display: inline-block;
    ">
    ➕ View All Frequently Asked Questions
    </a>
</div>
""", unsafe_allow_html=True)

# Add some sample questions as plain text (no expanders)
st.markdown("### Most Common Questions")

st.markdown("#### 💼 Why Choose AI Voice Agents?")
st.markdown("""
**What exactly is an AI Voice Representative?**

AI Voice Representatives are cutting-edge virtual agents that revolutionize how businesses handle communications. They conduct remarkably natural phone conversations, answer complex questions, process requests, and deliver consistent excellence 24/7/365.

**How do AI Voice Agents differ from traditional IVR systems?**

Unlike traditional IVR systems that force callers through rigid menu trees, our AI Voice Agents engage in natural conversations. They don't just recognize keywords—they understand intent, can handle complex inquiries, and provide personalized responses that sound human, creating a dramatically improved customer experience.
""")

st.markdown("#### 💰 Cost Savings & Benefits")
st.markdown("""
**What kind of cost savings can I expect?**

Businesses typically slash communication costs by 50-70% when implementing AI Voice Agents. Beyond the obvious savings on salaries and benefits, you'll eliminate costly overhead from recruitment, training, absenteeism, and management.

**How do AI Voice Agents improve operational efficiency?**

Our AI Voice Agents provide 24/7/365 availability, infinite scalability, zero ramp-up time, perfect consistency, and instant knowledge updates across your entire system.
""")

# Add link to contact for more information
st.markdown("""
<div style="text-align: center; margin-top: 20px; margin-bottom: 30px;">
    <p style="color: #AAA; font-size: 16px;">
        For more information and a complete list of FAQs, please 
        <a href="https://www.connexus.ai/contact" style="color: #00FFAA; text-decoration: none; font-weight: 500;">contact us</a>.
    </p>
</div>
""", unsafe_allow_html=True)
