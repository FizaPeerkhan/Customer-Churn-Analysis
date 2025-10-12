import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def show_business_problem():
    
    # Header with Netflix style
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #000000 0%, #E50914 100%); border-radius: 10px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0;'>🎬 THE STREAMING CHURN CRISIS</h1>
        <p style='color: #FFD700; margin: 5px 0 0 0; font-size: 1.2rem;'>Why Customer Retention is Netflix's Biggest Battle</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Problem Overview in Columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🏆 Market Position", 
            value="200+ Competitors",
            delta="5x growth since 2020"
        )
        
    with col2:
        st.metric(
            label="💸 Customer Value", 
            value="$180/yr",
            delta="-12% from 2022"
        )
        
    with col3:
        st.metric(
            label="📉 Churn Risk", 
            value="35% of Users",
            delta="+8% YoY"
        )
    
    st.markdown("---")
    
    # The Battlefield - Competition
    st.subheader("🎯 The Streaming Battlefield")
    
    # Competition chart
    competitors = ['Netflix', 'Disney+', 'Amazon Prime', 'HBO Max', 'Apple TV+', 'Hulu']
    subscribers = [247, 150, 200, 96, 40, 48]  # in millions
    churn_rates = [6.3, 4.8, 5.2, 7.1, 8.5, 9.2]  # monthly %
    
    fig = go.Figure(data=[
        go.Bar(name='Subscribers (M)', x=competitors, y=subscribers, marker_color='#E50914'),
        go.Bar(name='Monthly Churn %', x=competitors, y=churn_rates, marker_color='#FFD700', yaxis='y2')
    ])
    
    fig.update_layout(
        title='Streaming Wars: Subscribers vs Churn Rates',
        yaxis=dict(title='Subscribers (Millions)'),
        yaxis2=dict(title='Monthly Churn %', overlaying='y', side='right'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Why Churn Matters
    st.subheader("💥 The Domino Effect of Churn")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.error("""
        **Immediate Impact**
        - Direct revenue loss per subscriber
        - Wasted acquisition costs ($300-500 per customer)
        - Reduced content investment ROI
        - Negative word-of-mouth
        """)
        
    with col2:
        st.warning("""
        **Long-term Consequences**
        - Stagnant growth in mature markets
        - Increased pressure to raise prices
        - Difficulty justifying content budgets
        - Investor confidence erosion
        """)
    
    # Churn Drivers
    st.subheader("🔍 What Makes Viewers Leave?")
    
    # Churn drivers visualization
    drivers = ['Price Increases', 'Content Gaps', 'Technical Issues', 'Competitor Offers', 'Account Sharing Crackdown']
    impact = [45, 30, 12, 28, 25]  # percentage impact
    
    fig2 = px.bar(
        x=impact, 
        y=drivers, 
        orientation='h',
        title='Top Churn Drivers (% Impact)',
        color=impact,
        color_continuous_scale='reds'
    )
    
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis_title='Impact Percentage',
        yaxis_title=''
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Netflix's Defense Strategy
    st.subheader("🛡️ Netflix's Multi-Layered Defense")
    
    tabs = st.tabs(["🎬 Content Strategy", "💳 Pricing Tactics", "🔧 Technical Edge", "📊 Data Science"])
    
    with tabs[0]:
        st.success("""
        **Content Fortress Strategy**
        - $17B annual content budget
        - Localized originals for each market
        - Continuous release calendar (no dry spells)
        - Genre diversification (K-dramas, Anime, Reality)
        - Interactive storytelling experiments
        """)
        
    with tabs[1]:
        st.info("""
        **Smart Pricing & Packaging**
        - Tiered plans (Basic: $7, Standard: $15, Premium: $23)
        - Family sharing (up to 5 profiles)
        - Mobile-only plans in emerging markets
        - Partner bundles (with telcos, device makers)
        """)
        
    with tabs[2]:
        st.warning("""
        **Technical Superiority**
        - Industry-leading streaming quality
        - Advanced recommendation engine
        - Offline downloads capability
        - Seamless multi-device experience
        - Personalized user interfaces
        """)
        
    with tabs[3]:
        st.error("""
        **Data-Driven Insights**
        - Real-time viewing analytics
        - Predictive churn modeling
        - A/B testing everything
        - Content performance tracking
        - Regional preference mapping
        """)
    
    # Our Solution Impact
    st.subheader("🚀 How Our Solution Changes the Game")
    
    # Before-After comparison
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 15px; background: #2D2D2D; border-radius: 10px;'>
            <h3 style='color: #E50914;'>🔮 Predictive Power</h3>
            <p>Identify at-risk customers 30 days before they churn</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 15px; background: #2D2D2D; border-radius: 10px;'>
            <h3 style='color: #1DB954;'>🎯 Precision Targeting</h3>
            <p>Right message to right user at right time</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 15px; background: #2D2D2D; border-radius: 10px;'>
            <h3 style='color: #FFD700;'>📈 ROI Maximization</h3>
            <p>Optimize $500M+ retention budget</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Expected Results
    st.subheader("📊 Projected Business Impact")
    
    # Results visualization
    metrics = {
        'Monthly Churn Rate': {'current': 6.3, 'target': 4.8},
        'Customer Lifetime Value': {'current': 42, 'target': 58},
        'Retention Campaign ROI': {'current': 180, 'target': 320},
        'At-risk Save Rate': {'current': 15, 'target': 45}
    }
    
    for metric, values in metrics.items():
        current = values['current']
        target = values['target']
        improvement = ((target - current) / current) * 100
        
        st.write(f"**{metric}**")
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.progress(target/100 if metric != 'Retention Campaign ROI' else target/500)
            
        with col2:
            st.write(f"{current} → {target}")
            
        with col3:
            st.write(f"📈 {improvement:+.1f}%")
    
    # Call to Action
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #E50914 0%, #B81D24 100%); border-radius: 15px;'>
        <h2 style='color: white; margin: 0;'>🎬 Ready to Win the Retention War?</h2>
        <p style='color: #FFD700; font-size: 1.2rem;'>Turn churn prediction into competitive advantage</p>
    </div>
    """, unsafe_allow_html=True)
