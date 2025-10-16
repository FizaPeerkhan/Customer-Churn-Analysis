import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def show_batch_results(df):
    # Netflix-style header
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #000000 0%, #E50914 100%); border-radius: 10px; margin-bottom: 20px;'>
        <h2 style='color: white; margin: 0;'>📊 BATCH ANALYSIS RESULTS</h2>
        <p style='color: #FFD700; margin: 5px 0 0 0;'>Complete Customer Data with AI Predictions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary metrics
    total_customers = len(df)
    high_risk_count = len(df[df['churn_prob'] > 70])
    medium_risk_count = len(df[(df['churn_prob'] >= 30) & (df['churn_prob'] <= 70)])
    avg_churn_prob = df['churn_prob'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Customers", total_customers)
    with col2:
        st.metric("High Risk", high_risk_count, delta=f"{high_risk_count/total_customers*100:.1f}%")
    with col3:
        st.metric("Medium Risk", medium_risk_count, delta=f"{medium_risk_count/total_customers*100:.1f}%")
    with col4:
        st.metric("Avg Churn Prob", f"{avg_churn_prob:.1f}%")
    
    st.markdown("---")
    
    # 🎯 MAIN RESULTS TABLE - AUTOMATICALLY DISPLAYED
    st.markdown("#### 👥 Complete Analysis Results")
    st.markdown("**All customer data with AI predictions and recommendations**")
    
    # Interactive filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        risk_filter = st.selectbox(
            "Risk Level",
            ["All", "High Risk (>70%)", "Medium Risk (30-70%)", "Low Risk (<30%)"],
            key="risk_filter"
        )
    
    with col2:
        segment_filter = st.selectbox(
            "Customer Segment",
            ["All", "Segment 0", "Segment 1", "Segment 2", "Segment 3"],
            key="segment_filter"
        )
    
    with col3:
        subscription_filter = st.selectbox(
            "Subscription Type",
            ["All", "Basic", "Standard", "Premium"],
            key="subscription_filter"
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if risk_filter == "High Risk (>70%)":
        filtered_df = filtered_df[filtered_df['churn_prob'] > 70]
    elif risk_filter == "Medium Risk (30-70%)":
        filtered_df = filtered_df[(filtered_df['churn_prob'] >= 30) & (filtered_df['churn_prob'] <= 70)]
    elif risk_filter == "Low Risk (<30%)":
        filtered_df = filtered_df[filtered_df['churn_prob'] < 30]
    
    if segment_filter != "All":
        segment_num = int(segment_filter.split(" ")[1])
        filtered_df = filtered_df[filtered_df['segment'] == segment_num]
    
    if subscription_filter != "All":
        filtered_df = filtered_df[filtered_df['subscription_type'] == subscription_filter]
    
    st.markdown(f"**Showing {len(filtered_df)} of {total_customers} customers**")
    
    # Create comprehensive display dataframe
    display_columns = [
        'age', 'gender', 'subscription_type', 'device', 'watch_hours', 
        'last_login_days', 'region', 'payment_method', 'number_of_profiles',
        'avg_watch_time_per_day', 'favorite_genre', 'segment', 'churn_prob', 'recommendation'
    ]
    
    # Filter to only include columns that exist in the dataframe
    available_columns = [col for col in display_columns if col in df.columns]
    display_df = filtered_df[available_columns].copy()
    
    # Format numerical columns
    if 'churn_prob' in display_df.columns:
        display_df['churn_prob'] = display_df['churn_prob'].round(1)
    if 'watch_hours' in display_df.columns:
        display_df['watch_hours'] = display_df['watch_hours'].round(1)
    if 'avg_watch_time_per_day' in display_df.columns:
        display_df['avg_watch_time_per_day'] = display_df['avg_watch_time_per_day'].round(1)
    
    # Add risk level column
    def get_risk_level(prob):
        if prob > 70:
            return "🔴 High"
        elif prob >= 30:
            return "🟡 Medium"
        else:
            return "🟢 Low"
    
    if 'churn_prob' in display_df.columns:
        display_df['risk_level'] = display_df['churn_prob'].apply(get_risk_level)
    
    # Reorder columns to put predictions at the end
    prediction_columns = ['segment', 'risk_level', 'churn_prob', 'recommendation']
    other_columns = [col for col in display_df.columns if col not in prediction_columns]
    final_columns = other_columns + [col for col in prediction_columns if col in display_df.columns]
    display_df = display_df[final_columns]
    
    # Rename columns for better display
    column_rename_map = {
        'age': 'Age',
        'gender': 'Gender', 
        'subscription_type': 'Subscription',
        'device': 'Device',
        'watch_hours': 'Watch Hours',
        'last_login_days': 'Last Login',
        'region': 'Region',
        'payment_method': 'Payment Method',
        'number_of_profiles': 'Profiles',
        'avg_watch_time_per_day': 'Avg Watch/Day',
        'favorite_genre': 'Favorite Genre',
        'segment': 'Segment',
        'risk_level': 'Risk Level',
        'churn_prob': 'Churn %',
        'recommendation': 'Recommendation'
    }
    
    display_df = display_df.rename(columns=column_rename_map)
    
    # 🎯 DISPLAY THE MAIN TABLE AUTOMATICALLY
    st.dataframe(
        display_df,
        use_container_width=True,
        height=500,
        column_config={
            "Age": st.column_config.NumberColumn(format="%d"),
            "Churn %": st.column_config.ProgressColumn(
                format="%.1f%%",
                min_value=0,
                max_value=100,
            ),
            "Watch Hours": st.column_config.NumberColumn(format="%.1f h"),
            "Avg Watch/Day": st.column_config.NumberColumn(format="%.1f h"),
            "Last Login": st.column_config.NumberColumn(format="%d days"),
            "Profiles": st.column_config.NumberColumn(format="%d"),
            "Risk Level": st.column_config.TextColumn(),
            "Segment": st.column_config.NumberColumn(format="%d"),
            "Recommendation": st.column_config.TextColumn(width="large")
        }
    )
    
    # Quick insights
    st.markdown("---")
    st.markdown("#### 📈 Quick Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk distribution
        if 'Risk Level' in display_df.columns:
            risk_counts = display_df['Risk Level'].value_counts()
            st.metric("Highest Risk Group", f"{risk_counts.index[0] if len(risk_counts) > 0 else 'N/A'}")
    
    with col2:
        # Most common recommendation
        if 'Recommendation' in display_df.columns:
            top_recommendation = display_df['Recommendation'].mode()
            if len(top_recommendation) > 0:
                st.metric("Top Recommendation", top_recommendation[0][:30] + "..." if len(top_recommendation[0]) > 30 else top_recommendation[0])
    
    # Export options
    st.markdown("---")
    st.markdown("#### 📤 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Results",
            data=csv,
            file_name="netflix_churn_analysis.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        full_csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Analysis",
            data=full_csv,
            file_name="netflix_complete_analysis.csv",
            mime="text/csv",
            use_container_width=True
        )