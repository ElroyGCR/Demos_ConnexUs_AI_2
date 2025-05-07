# Add this at the end of your calculator script, right before the final spacing div

# ─── FAQ Section with Compact Design ────────────────────
st.markdown("---")

# FAQ Header
section_header("Frequently Asked Questions")

# Header description
st.markdown("""
<div style="background-color: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px; margin-bottom: 15px;">
    <p style="color: #ffffff; font-size: 16px; margin: 0;">
        Common questions about AI automation and how it can benefit your contact center operations.
    </p>
</div>
""", unsafe_allow_html=True)

# Master FAQ expander - contains all other FAQ categories
with st.expander("➕ Show All FAQs"):
    # Use tabs to create a more compact FAQ section
    faq_tabs = st.tabs([
        "Why Choose AI", 
        "Cost & Efficiency", 
        "Implementation", 
        "Capabilities",
        "Customer Experience",
        "Security",
        "Getting Started"
    ])
    
    # Tab 1: Why Businesses Are Switching to AI Voice Agents
    with faq_tabs[0]:
        with st.expander("What exactly is an AI Voice Representative?"):
            st.write("""
            • AI Voice Representatives are cutting-edge virtual agents that revolutionize how businesses handle communications. They conduct remarkably natural phone conversations, answer complex questions, process requests, and deliver consistent excellence 24/7/365. 
            
            • Unlike human agents who need breaks, vacations, and sick days, our AI Voice Representatives work around the clock with zero downtime, zero turnover, and zero training requirements—transforming your customer service from a cost center into a competitive advantage.
            """)

        with st.expander("How do AI Voice Agents differ from traditional IVR systems?"):
            st.write("""
            • Unlike traditional IVR systems that force callers through rigid menu trees, our AI Voice Agents engage in natural conversations. They don't just recognize keywords—they understand intent, can handle complex inquiries, and provide personalized responses that sound human, creating a dramatically improved customer experience.
            """)

    # Tab 2: Cost Savings & Operational Efficiency
    with faq_tabs[1]:
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

    # Tab 3: Implementation & Integration
    with faq_tabs[2]:
        with st.expander("How long does it take to implement AI Voice Agents?"):
            st.write("""
            • Implementation timelines depend on the specific product type you choose and your business requirements. Many of our solutions can be deployed rapidly with minimal setup time. 
            
            • For detailed information about implementation for your specific needs, please contact us through our website at www.connexus.ai.
            """)

        with st.expander("Will AI Voice Agents integrate with my existing systems?"):
            st.write("""
            • Absolutely! Our flexible integration framework connects with virtually any business system you're currently using. Whether it's a popular CRM like Salesforce, your proprietary databases, or legacy phone systems, we design custom integration pathways that make implementation smooth and non-disruptive. 
            
            • Contact us at www.connexus.ai for a personalized integration assessment.
            """)

    # Tab 4: Capabilities & Limitations
    with faq_tabs[3]:
        with st.expander("What types of calls can AI Voice Agents handle effectively?"):
            st.write("""
            • Our AI Voice Agents excel at handling appointment scheduling, customer service inquiries, order status updates, product information requests, lead qualification, and routine transactions. They're particularly effective for high-volume, repetitive call types that follow predictable patterns.
            """)

        with st.expander("How do AI Voice Agents handle complex or unusual customer requests?"):
            st.write("""
            • Our AI Voice Agents are designed to recognize when a conversation exceeds their capabilities. In these situations, they seamlessly transfer the call to a human agent, providing a complete transcript and summary of the conversation so the human agent can pick up exactly where the AI left off—creating a smooth customer experience.
            """)

        with st.expander("Can AI Voice Agents make outbound calls too?"):
            st.write("""
            • Absolutely! Our AI Voice Agents can conduct outbound calling campaigns for appointment reminders, payment collection, satisfaction surveys, lead qualification, and promotional offers. They can reach hundreds of customers simultaneously with personalized conversations that drive results.
            """)

    # Tab 5: Quality & Customer Experience
    with faq_tabs[4]:
        with st.expander("How natural do the AI Voice Agents sound?"):
            st.write("""
            • Our advanced AI technology produces remarkably natural-sounding voices that many callers cannot distinguish from humans. The agents understand context, respond to emotional cues, adjust their tone appropriately, and can even insert thoughtful pauses and conversational fillers for an authentic experience.
            """)

        with st.expander("What languages do your AI Voice Agents support?"):
            st.write("""
            • Our AI Voice Agents currently support over 25 languages including English, Spanish, French, German, Italian, Portuguese, Mandarin, Japanese, and Arabic. Each language version maintains natural intonation and cultural nuances for an authentic experience regardless of region.
            """)

        with st.expander("How do customers typically react to AI Voice Agents?"):
            st.write("""
            • Customer satisfaction scores with our AI Voice Agents average 4.7/5 across industries. Customers particularly appreciate the instant response (no hold times), 24/7 availability, and consistent experience. In blind tests, over 60% of customers couldn't tell they were speaking with an AI agent.
            """)

    # Tab 6: Security & Compliance
    with faq_tabs[5]:
        with st.expander("How secure is the AI Voice Agent solution?"):
            st.write("""
            • Our AI Voice Agent platform is built with enterprise-grade security. All conversations are encrypted end-to-end, we maintain SOC 2 Type II compliance, and can support industry-specific requirements like HIPAA for healthcare and PCI DSS for payment processing. Your data and your customers' information remains secure at all times.
            """)

        with st.expander("Do AI Voice Agents comply with disclosure requirements?"):
            st.write("""
            • Yes. Our AI Voice Agents can be configured to disclose their virtual nature at the beginning of calls in compliance with emerging AI transparency regulations. This disclosure can be customized based on your preferences and regulatory requirements in your operating regions.
            """)

    # Tab 7: Getting Started
    with faq_tabs[6]:
        with st.expander("How can I see your AI Voice Agents in action?"):
            st.write("""
            • Experience our AI Voice Agents firsthand with our interactive demo right on this website. Better yet, schedule a personalized demonstration where we'll show you exactly how our technology can transform your specific business operations, handling your unique call scenarios with precision and natural conversation flow.
            """)

        with st.expander("How is pricing structured for AI Voice Agents?"):
            st.write("""
            • Pricing depends on the specific product package that best fits your business needs. Unlike traditional call centers with unpredictable staffing costs, our pricing models offer predictability and transparency. Many clients find our ROI calculator eye-opening when they see the potential cost savings. 
            
            • For detailed pricing information tailored to your requirements, please contact us through our website at www.connexus.ai.
            """)

        with st.expander("What's the first step in getting started with AI Voice Agents?"):
            st.write("""
            • The best way to begin is by scheduling a free consultation through our website at www.connexus.ai. Our experts will assess your current call operations, identify opportunities for AI implementation, and provide a customized proposal showing expected cost savings and performance improvements specific to your business model.
            """)

# Add some spacing at the bottom
st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
