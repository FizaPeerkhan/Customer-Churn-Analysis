import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from segmentation import assign_cluster
from prediction import predict_churn
from recommendation import recommend_offer

# --- Streamlit page config ---
st.set_page_config(page_title="Netflix Customer Insights", page_icon="🎬", layout="wide")

st.markdown("<h1 style='color: red;'>🎬 Netflix Customer Insights</h1>", unsafe_allow_html=True)
st.markdown("Predict customer segment, churn probability, and get recommendations. Upload CSV for batch insights!")

# --- Cluster insights mapping ---
cluster_insights = {
    0: {"title": "🟢 Inactive Premium Tablet Users",
        "description": "Dormant Premium users — low engagement, rarely watch content. High churn risk.\n\n"
                       "Action: Send win-back campaigns, personalized drama content, offer discounts or trial extensions."},
    1: {"title": "🔵 Active Premium Mobile Users",
        "description": "Highly engaged Premium users, regularly consuming content on mobile.\n\n"
                       "Action: Encourage loyalty, push new Sci-Fi releases, suggest family profile features."},
    2: {"title": "🔴 Power Basic Desktop Users",
        "description": "Extremely active Basic users — high watch hours, family-type usage.\n\n"
                       "Action: Upsell to Premium, highlight multiple-screen features, recommend documentaries."},
    3: {"title": "🟡 Semi-active Premium Laptop Users",
        "description": "Moderate engagement — long gaps between sessions.\n\n"
                       "Action: Re-engage with personalized recommendations or notifications."}
}

st.markdown("---")
st.subheader("📝 Single Customer Prediction")

# --- Single customer form ---
with st.form("customer_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", 10, 80, 30)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        region = st.selectbox("Region", ["Africa", "Europe", "Asia", "Oceania", "America"])
        number_of_profiles = st.number_input("Number of Profiles", 1, 5)
    with col2:
        subscription_type = st.selectbox("Subscription Type", ["Basic", "Standard", "Premium"])
        device = st.selectbox("Device", ["TV", "Mobile", "Tablet", "Laptop"])
        payment_method = st.selectbox("Payment Method", ["Gift Card", "Credit Card", "Crypto", "Bank Transfer"])
    with col3:
        watch_hours = st.number_input("Total Watch Hours", min_value=0.0, step=0.1)
        avg_watch_time_per_day = st.number_input("Avg Watch Time Per Day (hrs)", min_value=0.0, step=0.1)
        last_login_days = st.number_input("Days Since Last Login", 0, 60)
        favorite_genre = st.selectbox("Favorite Genre", ["Action", "Drama", "Horror", "Sci-Fi", "Comedy", "Romance"])
    submitted = st.form_submit_button("🔍 Predict Segment & Churn")

if submitted:
    user_input = pd.DataFrame([[age, gender, subscription_type, watch_hours, last_login_days,
                                region, device, payment_method, number_of_profiles,
                                avg_watch_time_per_day, favorite_genre]],
                              columns=["age", "gender", "subscription_type", "watch_hours", "last_login_days",
                                       "region", "device", "payment_method", "number_of_profiles",
                                       "avg_watch_time_per_day", "favorite_genre"])
    try:
        # Segment
        cluster_label = assign_cluster(user_input)
        insight = cluster_insights.get(cluster_label, {"title": "Unknown", "description": "No info."})
        st.success(f"🎯 Segment: **{insight['title']}**")
        st.info(insight['description'])

        # Churn
        churn_result = predict_churn(user_input)
        churn_text = "Churn" if churn_result['predicted_class'] == 1 else "No Churn"
        st.success(f"📊 Churn Prediction: **{churn_text}**")
        st.info(f"Churn Probability: {churn_result['churn_probability']}%")

        # Recommendation
        recommendation = recommend_offer(cluster_label, churn_result['churn_probability'], subscription_type)
        st.markdown("---")
        st.subheader("🎁 Recommended Action")
        st.markdown(f"**{recommendation}**")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

st.markdown("---")
st.subheader("📂 Batch Prediction via CSV Upload")

uploaded_file = st.file_uploader("Upload CSV with customer data", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.info("✅ CSV uploaded successfully!")

    # Helper to ensure column ordering for each row
    cols = ["age", "gender", "subscription_type", "watch_hours", "last_login_days",
            "region", "device", "payment_method", "number_of_profiles",
            "avg_watch_time_per_day", "favorite_genre"]
    def single_row_df(row):
        return pd.DataFrame([row[cols].tolist()], columns=cols)

    # Apply predictions for all rows
    df['segment'] = df.apply(lambda row: assign_cluster(single_row_df(row)), axis=1)
    df['churn_prob'] = df.apply(lambda row: predict_churn(single_row_df(row))['churn_probability'], axis=1)
    df['recommendation'] = df.apply(lambda row: recommend_offer(row['segment'], row['churn_prob'], row['subscription_type']), axis=1)

    st.markdown("### Batch Results Table")
    st.dataframe(df)

    # --- Visual Insights ---
    st.markdown("### Visual Insights")
    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(3.5, 2.5))
        sns.countplot(x='segment', data=df, palette='Set2', ax=ax)
        ax.set_title("Customer Segment Distribution", fontsize=12, weight='bold', pad=8)
        ax.set_xlabel("Segment", fontsize=10)
        ax.set_ylabel("Count", fontsize=10)
        ax.tick_params(axis='x', labelsize=9)
        ax.tick_params(axis='y', labelsize=9)
        for spine in ax.spines.values():
            spine.set_visible(False)
        for p in ax.patches:
            _x = p.get_x() + p.get_width() / 2
            _y = p.get_height()
            if _y > 0:
                ax.annotate(f"{int(_y)}", (_x, _y), ha='center', va='bottom', fontsize=9, color='black')
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(3.5, 2.5))
        sns.histplot(df['churn_prob'], bins=10, kde=True, color='#e74c3c', ax=ax2, edgecolor='#222')
        ax2.set_title("Churn Probability Distribution", fontsize=12, weight='bold', pad=8)
        ax2.set_xlabel("Churn Probability (%)", fontsize=10)
        ax2.set_ylabel("Count", fontsize=10)
        ax2.tick_params(axis='x', labelsize=9)
        ax2.tick_params(axis='y', labelsize=9)
        for spine in ax2.spines.values():
            spine.set_visible(False)
        plt.tight_layout()
        st.pyplot(fig2)

    # --- Key Metrics ---
    st.markdown("### 🌟 Key Metrics")
    mcol1, mcol2, mcol3 = st.columns(3)
    min_height = "180px"

    # Total Users
    with mcol1:
        st.markdown(f"""
        <div style="
            background-color:#141414;
            border-radius:12px;
            padding:20px;
            min-height:{min_height};
            text-align:center;
            color:#fff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
            <div style='font-size:32px;'>👥</div>
            <div style='font-size:16px; margin-top:8px; font-weight:bold;'>Total Users</div>
            <div style='font-size:36px; color:#e50914; font-weight:bold;'>{len(df)}</div>
        </div>
        """, unsafe_allow_html=True)

    # High Churn Risk
    high_risk = (df['churn_prob'] > 70).sum()
    with mcol2:
        st.markdown(f"""
        <div style="
            background-color:#141414;
            border-radius:12px;
            padding:20px;
            min-height:{min_height};
            text-align:center;
            color:#fff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
            <div style='font-size:32px;'>⚠️</div>
            <div style='font-size:16px; margin-top:8px; font-weight:bold;'>High Churn Risk</div>
            <div style='font-size:36px; color:#f5c518; font-weight:bold;'>{high_risk}</div>
        </div>
        """, unsafe_allow_html=True)

    # Segment Breakdown
    seg_counts = df['segment'].value_counts().sort_index()
    max_count = seg_counts.max()
    bars_html = ""
    colors = ["#e50914", "#b81d24", "#f5c518", "#1db954"]
    for i, (seg, count) in enumerate(seg_counts.items()):
        width_percent = int((count / max_count) * 100)
        color = colors[i % len(colors)]
        bars_html += f"""
        <div style="margin-bottom:6px; text-align:left;">
            <span style='font-weight:bold;'>Seg {seg}: {count}</span>
            <div style='background-color:#333; border-radius:8px; height:12px; margin-top:2px;'>
                <div style='width:{width_percent}%; background-color:{color}; height:12px; border-radius:8px;'></div>
            </div>
        </div>
        """
    with mcol3:
        st.markdown(f"""
        <div style="
            background-color:#141414;
            border-radius:12px;
            padding:20px;
            min-height:{min_height};
            text-align:left;
            color:#fff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
            <div style='font-size:32px; text-align:center;'>✨</div>
            <div style='font-size:16px; margin-top:8px; font-weight:bold; text-align:center;'>Segment Breakdown</div>
            <div style='margin-top:12px;'>{bars_html}</div>
        </div>
        """, unsafe_allow_html=True)

    # --- Download CSV ---
    st.markdown("<br>", unsafe_allow_html=True)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Predictions CSV",
        data=csv,
        file_name="customer_predictions.csv",
        mime="text/csv"
    )
