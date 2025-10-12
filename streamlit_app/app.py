import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
import numpy as np

from segmentation import assign_cluster
from prediction import predict_churn
from recommendation import recommend_offer
from business_problem import show_business_problem
# --- Streamlit Page Config ---
st.set_page_config(
    page_title="Netflix Customer Insights", 
    page_icon="🎬", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Enhanced Netflix Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Helvetica+Neue:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    
    .main-header {
        font-size: 2.8rem;
        color: #E50914;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .sub-header {
        color: #E50914;
        border-bottom: 2px solid #E50914;
        padding-bottom: 0.5rem;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 1.5rem;
        letter-spacing: -0.3px;
    }
    .metric-card {
        background: linear-gradient(135deg, #141414 0%, #1a1a1a 100%);
        border-radius: 10px;
        padding: 18px;
        text-align: center;
        color: white;
        border: 1px solid #333;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(229, 9, 20, 0.2);
        border-color: #E50914;
    }
    .section-card {
        background: linear-gradient(135deg, #141414 0%, #1a1a1a 100%);
        border-radius: 10px;
        padding: 22px;
        border: 1px solid #333;
        margin: 12px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    .feature-list {
        text-align: left;
        background: linear-gradient(135deg, #1A1A1A 0%, #222 100%);
        padding: 18px;
        border-radius: 8px;
        margin: 12px 0;
        border-left: 4px solid #E50914;
        border: 1px solid #333;
    }
    .feature-list p {
        color: #FFFFFF;
        margin: 6px 0;
        font-size: 0.95rem;
        font-weight: 500;
    }
    .success-message {
        background: linear-gradient(135deg, #1A1A1A 0%, #1a2a1a 100%);
        border: 1px solid #1DB954;
        border-radius: 8px;
        padding: 18px;
        margin: 12px 0;
    }
    .info-message {
        background: linear-gradient(135deg, #1A1A1A 0%, #1a1a2a 100%);
        border: 1px solid #007BFF;
        border-radius: 8px;
        padding: 18px;
        margin: 12px 0;
    }
    
    /* Enhanced Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #141414;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #333;
    }
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        white-space: pre-wrap;
        background-color: #2D2D2D;
        border-radius: 8px;
        gap: 8px;
        padding: 0px 24px;
        font-weight: 600;
        font-size: 1rem;
        border: 1px solid transparent;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #3D3D3D;
        border-color: #666;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #E50914 0%, #B81D24 100%);
        color: white;
        border-color: #E50914;
        box-shadow: 0 4px 12px rgba(229, 9, 20, 0.3);
    }
    
    /* Enhanced Button Styling */
    .stButton button {
        background: linear-gradient(135deg, #E50914 0%, #B81D24 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 28px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(229, 9, 20, 0.3) !important;
    }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(229, 9, 20, 0.4) !important;
        background: linear-gradient(135deg, #B81D24 0%, #E50914 100%) !important;
    }
    
    /* Download Button Specific */
    .stDownloadButton button {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%) !important;
        box-shadow: 0 4px 12px rgba(29, 185, 84, 0.3) !important;
    }
    .stDownloadButton button:hover {
        background: linear-gradient(135deg, #1ed760 0%, #1DB954 100%) !important;
        box-shadow: 0 6px 16px rgba(29, 185, 84, 0.4) !important;
    }
    
    /* Custom header with Netflix logo */
    .netflix-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-bottom: 1rem;
    }
    .netflix-logo {
        font-size: 2.5rem;
        color: #E50914;
        font-weight: 900;
    }
    
    /* Enhanced metrics text */
    .metric-number {
        font-size: 2rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #CCCCCC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 8px 0 !important;
    }
    .metric-label {
        font-size: 0.9rem !important;
        color: #999 !important;
        font-weight: 600 !important;
        margin: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Configure matplotlib for professional look
plt.rcParams['figure.facecolor'] = '#141414'
plt.rcParams['axes.facecolor'] = '#141414'
plt.rcParams['axes.edgecolor'] = '#666666'
plt.rcParams['axes.labelcolor'] = '#FFFFFF'
plt.rcParams['text.color'] = '#FFFFFF'
plt.rcParams['xtick.color'] = '#FFFFFF'
plt.rcParams['ytick.color'] = '#FFFFFF'
plt.rcParams['grid.color'] = '#333333'
plt.rcParams['font.size'] = 9
plt.rcParams['figure.figsize'] = [6, 4]

# --- Load Model ---
try:
    model_path = os.path.join(os.path.dirname(__file__), "..", "models", "gb_churn_model.joblib")
    model = joblib.load(model_path)
except FileNotFoundError:
    st.error("Model not found. Ensure 'gb_churn_model.joblib' exists in 'models' directory.")
    st.stop()

# --- Enhanced Header with Netflix Logo ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class='netflix-header'>
        <div class='netflix-logo'>N</div>
        <div>
            <h1 class='main-header'> 🎬 Netflix Customer Insights</h1>
            <p style='text-align: center; color: #888; margin: 0; font-weight: 500; letter-spacing: 0.5px;'>
            Advanced Analytics • Churn Prediction • Personalized Experiences
            </p>
        </div>
        <div class='netflix-logo' style='transform: scaleX(-1);'>N</div>
    </div>
    """, unsafe_allow_html=True)

# --- Cluster Insights ---
cluster_insights = {
    0: {"title": "Inactive Premium Tablet Users",
        "description": "Dormant Premium users with low engagement. High churn risk."},
    1: {"title": "Active Premium Mobile Users", 
        "description": "Highly engaged Premium users on mobile devices."},
    2: {"title": "Power Basic Desktop Users",
        "description": "Active Basic users with high watch hours."},
    3: {"title": "Semi-active Premium Laptop Users",
        "description": "Moderate engagement with long gaps between sessions."}
}

# --- Main Content with Enhanced Tabs ---
tab1, tab2, tab3 = st.tabs(["🎯 SINGLE ANALYSIS", "📊 BATCH ANALYSIS", "💼 BUSINESS PROBLEM"])

# Add the business problem tab
with tab3:
    show_business_problem()

with tab1:
    st.markdown("<h3 class='sub-header'>Individual Customer Analysis</h3>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**👤 Personal Details**")
            age = st.number_input("Age", 10, 80, 30, key="age_single")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="gender_single")
            region = st.selectbox("Region", ["Africa", "Europe", "Asia", "Oceania", "America"], key="region_single")
            number_of_profiles = st.number_input("Number of Profiles", 1, 5, 1, key="profiles_single")
            
        with col2:
            st.markdown("**💳 Subscription Details**")
            subscription_type = st.selectbox("Subscription Type", ["Basic", "Standard", "Premium"], key="sub_single")
            device = st.selectbox("Primary Device", ["TV", "Mobile", "Tablet", "Laptop"], key="device_single")
            payment_method = st.selectbox("Payment Method", ["Gift Card", "Credit Card", "Crypto", "Bank Transfer"], key="payment_single")
            favorite_genre = st.selectbox("Favorite Genre", ["Action", "Drama", "Horror", "Sci-Fi", "Comedy", "Romance"], key="genre_single")
            
        with col3:
            st.markdown("**📈 Engagement Metrics**")
            watch_hours = st.number_input("Total Watch Hours", min_value=0.0, step=0.1, value=50.0, key="watch_single")
            avg_watch_time_per_day = st.number_input("Avg Watch Time (hrs)", min_value=0.0, step=0.1, value=2.5, key="avg_single")
            last_login_days = st.number_input("Days Since Last Login", 0, 60, 7, key="login_single")
    
    # Centered Analyze Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_clicked = st.button("🚀 **ANALYZE CUSTOMER**", use_container_width=True, type="primary")
    
    if analyze_clicked:
        user_input = pd.DataFrame([[age, gender, subscription_type, watch_hours, last_login_days,
                                    region, device, payment_method, number_of_profiles,
                                    avg_watch_time_per_day, favorite_genre]],
                                columns=["age","gender","subscription_type","watch_hours","last_login_days",
                                         "region","device","payment_method","number_of_profiles",
                                         "avg_watch_time_per_day","favorite_genre"])
        try:
            # Results in columns
            col1, col2 = st.columns(2)
            
            with col1:
                cluster_label = assign_cluster(user_input)
                insight = cluster_insights.get(cluster_label, {"title": "Unknown", "description": "No info."})
                st.markdown(f"""
                <div class='info-message'>
                    <h4 style='color: #007BFF; margin-bottom: 12px;'>🎯 CUSTOMER SEGMENT</h4>
                    <p style='font-weight: 600; font-size: 1.1rem; margin-bottom: 8px;'>{insight['title']}</p>
                    <p style='color: #CCC;'>{insight['description']}</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                churn_result = predict_churn(user_input)
                churn_text = "HIGH CHURN RISK" if churn_result['predicted_class'] == 1 else "LOW CHURN RISK"
                color = "#E50914" if churn_result['predicted_class'] == 1 else "#1DB954"
                icon = "⚠️" if churn_result['predicted_class'] == 1 else "✅"
                st.markdown(f"""
                <div class='success-message' style='border-color: {color};'>
                    <h4 style='color: {color}; margin-bottom: 12px;'>📊 CHURN PREDICTION</h4>
                    <p style='font-weight: 700; font-size: 1.2rem; color: {color}; margin-bottom: 8px;'>{icon} {churn_text}</p>
                    <p style='color: #CCC; font-size: 1.1rem;'>Probability: <strong>{churn_result['churn_probability']}%</strong></p>
                </div>
                """, unsafe_allow_html=True)

            # Recommendation
            recommendation = recommend_offer(cluster_label, churn_result['churn_probability'], subscription_type)
            st.markdown(f"""
            <div class='section-card'>
                <h4 style='color: #E50914; margin-bottom: 12px;'>🎁 RECOMMENDED ACTION</h4>
                <p style='font-size: 1.1rem; font-weight: 500;'>{recommendation}</p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Analysis error: {e}")

with tab2:
    st.markdown("<h3 class='sub-header'>Batch Customer Analysis</h3>", unsafe_allow_html=True)
    
    # Enhanced Upload Section
    st.markdown("""
    <div class='section-card'>
        <h4 style='color: #E50914; margin-bottom: 15px;'>📁 UPLOAD CUSTOMER DATA</h4>
        <p style='color: #CCC; margin-bottom: 15px;'>Upload a CSV file containing customer data for batch analysis and insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose CSV file", type=["csv"], label_visibility="collapsed")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        st.markdown(f"""
        <div class='success-message'>
            <h4 style='color: #1DB954; margin-bottom: 8px;'>✅ FILE UPLOADED SUCCESSFULLY</h4>
            <p style='color: #CCC; margin: 0;'><strong>{len(df)}</strong> customer records loaded • <strong>{len(df.columns)}</strong> columns detected</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Process data
        cols = ["age", "gender", "subscription_type", "watch_hours", "last_login_days",
                "region", "device", "payment_method", "number_of_profiles",
                "avg_watch_time_per_day", "favorite_genre"]

        def single_row_df(row):
            return pd.DataFrame([row[cols].tolist()], columns=cols)

        # Progress with enhanced styling
        with st.spinner('🔄 Processing customer data...'):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔍 Analyzing customer segments...")
            df['segment'] = df.apply(lambda row: assign_cluster(single_row_df(row)), axis=1)
            progress_bar.progress(0.33)
            
            status_text.text("📈 Calculating churn probabilities...")
            df['churn_prob'] = df.apply(lambda row: predict_churn(single_row_df(row))['churn_probability'], axis=1)
            progress_bar.progress(0.66)
            
            status_text.text("🎯 Generating recommendations...")
            df['recommendation'] = df.apply(lambda row: recommend_offer(row['segment'], row['churn_prob'], row['subscription_type']), axis=1)
            progress_bar.progress(1.0)
            
            status_text.text("✅ Analysis complete!")

        # Add revenue calculations
        if 'monthly_revenue' not in df.columns:
            df['monthly_revenue'] = 499
        df['revenue_loss'] = (df['churn_prob'] / 100) * df['monthly_revenue']
        
        # Simulate churn probability after recommendations
        df['churn_prob_after'] = df['churn_prob'] * np.random.uniform(0.6, 0.9, len(df))
        
        # Enhanced Results section
        st.markdown("#### 📊 Analysis Overview")
        
        # Enhanced Key Metrics
        total_users = len(df)
        high_risk_users = (df['churn_prob'] > 70).sum()
        medium_risk_users = ((df['churn_prob'] >= 30) & (df['churn_prob'] <= 70)).sum()
        avg_churn = df['churn_prob'].mean()
        total_revenue_loss = df['revenue_loss'].sum()
        avg_revenue_per_user = total_revenue_loss / total_users if total_users > 0 else 0
        
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>TOTAL USERS</div>
                <div class='metric-number'>{total_users}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>HIGH RISK USERS</div>
                <div class='metric-number'>{high_risk_users}</div>
                <div class='metric-label'>{medium_risk_users} medium risk</div>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_col3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>AVG CHURN RATE</div>
                <div class='metric-number'>{avg_churn:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_col4:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>REVENUE AT RISK</div>
                <div class='metric-number'>₹{total_revenue_loss:,.0f}</div>
                <div class='metric-label'>₹{avg_revenue_per_user:.0f}/user</div>
            </div>
            """, unsafe_allow_html=True)

        # Batch Results Overview Section
        st.markdown("---")
        st.markdown("#### 📈 BATCH RESULTS OVERVIEW")
        
        # Row 1: Customer Segments and Churn Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("🎯 CUSTOMER SEGMENTS", expanded=True):
                fig1, ax1 = plt.subplots(figsize=(6, 4))
                segment_counts = df['segment'].value_counts().sort_index()
                colors = ['#E50914', '#1DB954', '#FFD700', '#007BFF']
                bars = ax1.bar(segment_counts.index.astype(str), segment_counts.values, color=colors, alpha=0.9)
                ax1.set_xlabel('Segment ID', fontweight=600)
                ax1.set_ylabel('Number of Customers', fontweight=600)
                ax1.set_title('Customer Segments Distribution', fontweight=700, pad=15)
                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                            f'{int(height)}', ha='center', va='bottom', fontweight=600, color='white')
                st.pyplot(fig1)
        
        with col2:
            with st.expander("📊 CHURN ANALYSIS", expanded=True):
                # Compact churn distribution
                fig2, ax2 = plt.subplots(figsize=(6, 4))
                n, bins, patches = ax2.hist(df['churn_prob'], bins=8, color='#E50914', alpha=0.8, edgecolor='white', linewidth=1)
                ax2.set_xlabel('Churn Probability (%)', fontweight=600)
                ax2.set_ylabel('Number of Customers', fontweight=600)
                ax2.set_title('Churn Distribution', fontweight=700, pad=12)
                st.pyplot(fig2)

        # Row 2: Feature Importance and Before/After Recommendations
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("🔍 FEATURE IMPORTANCE", expanded=True):
                fig3, ax3 = plt.subplots(figsize=(6, 4))
                feature_names = ["Age", "Gender", "Subscription", "Watch Hours", "Last Login",
                                "Region", "Device", "Payment", "Profiles", "Avg Watch", "Genre"]
                
                if hasattr(model, 'feature_importances_'):
                    importances = model.feature_importances_
                elif 'classifier' in model and hasattr(model['classifier'], 'feature_importances_'):
                    importances = model['classifier'].feature_importances_
                else:
                    importances = np.ones(len(feature_names)) / len(feature_names)

                importances = importances[:len(feature_names)]
                indices = np.argsort(importances)
                
                bars = ax3.barh(np.array(feature_names)[indices], importances[indices], 
                               color='#E50914', alpha=0.8)
                
                # Add value labels
                for i, (bar, importance) in enumerate(zip(bars, importances[indices])):
                    ax3.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2.,
                            f'{importance:.3f}', ha='left', va='center', fontweight=600, color='white', fontsize=8)
                
                ax3.set_xlabel('Importance Score', fontweight=600)
                ax3.set_title('Feature Importance for Churn Prediction', fontweight=700, pad=12)
                ax3.grid(True, alpha=0.3)
                st.pyplot(fig3)
        
        with col2:
            with st.expander("🔄 BEFORE/AFTER RECOMMENDATIONS", expanded=True):
                fig4, ax4 = plt.subplots(figsize=(6, 4))
                
                # Sample data for before/after comparison
                sample_size = min(50, len(df))
                sample_indices = np.random.choice(len(df), sample_size, replace=False)
                before_probs = df.iloc[sample_indices]['churn_prob'].values
                after_probs = df.iloc[sample_indices]['churn_prob_after'].values
                
                x = np.arange(sample_size)
                width = 0.35
                
                bars1 = ax4.bar(x - width/2, before_probs, width, label='Before', color='#E50914', alpha=0.8)
                bars2 = ax4.bar(x + width/2, after_probs, width, label='After', color='#1DB954', alpha=0.8)
                
                ax4.set_xlabel('Customer Sample', fontweight=600)
                ax4.set_ylabel('Churn Probability (%)', fontweight=600)
                ax4.set_title('Churn Probability: Before vs After Recommendations', fontweight=700, pad=12)
                ax4.legend(facecolor='#141414')
                ax4.set_xticks([])  # Remove x-axis ticks for cleaner look
                
                # Add average improvement text
                avg_improvement = ((before_probs - after_probs) / before_probs * 100).mean()
                ax4.text(0.02, 0.98, f'Avg Improvement: {avg_improvement:.1f}%', 
                        transform=ax4.transAxes, fontweight=600, color='#1DB954',
                        bbox=dict(boxstyle="round,pad=0.3", facecolor='#141414', alpha=0.8))
                
                st.pyplot(fig4)

        # Row 3: Revenue Impact and Risk Categories
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("💸 REVENUE IMPACT", expanded=True):
                fig5, ax5 = plt.subplots(figsize=(6, 4))
                revenue_by_segment = df.groupby('segment')['revenue_loss'].sum()
                colors = ['#E50914', '#1DB954', '#FFD700', '#007BFF']
                bars = ax5.bar(revenue_by_segment.index.astype(str), revenue_by_segment.values, 
                              color=colors, alpha=0.9)
                ax5.set_xlabel('Segment ID', fontweight=600)
                ax5.set_ylabel('Revenue at Risk (₹)', fontweight=600)
                ax5.set_title('Revenue Impact by Segment', fontweight=700, pad=12)
                
                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax5.text(bar.get_x() + bar.get_width()/2., height + 1000,
                            f'₹{height:,.0f}', ha='center', va='bottom', fontweight=600, color='white', fontsize=9)
                
                st.pyplot(fig5)
        
        with col2:
            with st.expander("⚠️ RISK CATEGORIES", expanded=True):
                # Risk categories pie chart
                low_risk = (df['churn_prob'] < 30).sum()
                medium_risk = ((df['churn_prob'] >= 30) & (df['churn_prob'] <= 70)).sum()
                high_risk = (df['churn_prob'] > 70).sum()
                
                fig6, ax6 = plt.subplots(figsize=(6, 4))
                sizes = [low_risk, medium_risk, high_risk]
                colors_pie = ['#1DB954', '#FFD700', '#E50914']
                labels = [f'Low Risk\n({low_risk})', f'Medium Risk\n({medium_risk})', f'High Risk\n({high_risk})']
                
                wedges, texts, autotexts = ax6.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%',
                                                  startangle=90, textprops={'color': 'white', 'fontweight': '600'})
                
                # Enhance the autopct text
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('600')
                
                ax6.set_title('Customer Risk Distribution', fontweight=700, pad=20, color='white')
                st.pyplot(fig6)

        # Enhanced Download section
        st.markdown("---")
        st.markdown("#### 📥 EXPORT RESULTS")
        
        st.markdown("""
        <div class='feature-list'>
            <p>• Customer segments and detailed profiles</p>
            <p>• Churn probability scores for each customer</p>
            <p>• Personalized retention recommendations</p>
            <p>• Revenue impact and risk analysis</p>
            <p>• Complete customer insights dataset</p>
        </div>
        """, unsafe_allow_html=True)
        
        csv_data = df.to_csv(index=False).encode('utf-8')
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="📊 DOWNLOAD ANALYSIS REPORT",
                data=csv_data,
                file_name="netflix_customer_insights.csv",
                mime="text/csv",
                use_container_width=True,
                key="download_batch"
            )

# --- Enhanced Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p style='margin: 0; font-weight: 500;'>Netflix Customer Insights Dashboard</p>
    <p style='margin: 5px 0 0 0; font-size: 0.9rem; color: #888;'>Advanced Analytics Platform</p>
</div>
""", unsafe_allow_html=True)