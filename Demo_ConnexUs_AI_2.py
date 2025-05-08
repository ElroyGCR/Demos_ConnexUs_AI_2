# This is just the FAQ section code - replace only this part in your working version

# ─── FAQ Section with Tabs and Collapsible Header ────────────────────
# Create a collapsible expander with the same header size as other sections
with st.expander("Frequently Asked Questions", expanded=False):
    # Simple text description with larger font
    st.write("Common questions about AI automation and how it can benefit your contact center operations.")

    # Use tabs to organize FAQs
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
