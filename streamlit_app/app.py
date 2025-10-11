import streamlit as st
import pandas as pd
from segmentation import assign_cluster
from prediction import predict_churn
from recommendation import recommend_offer  # ✅ New addition

# --- Streamlit page config ---
st.set_page_config(page_title="Netflix Customer Insights", page_icon="🎬", layout="wide")

st.markdown("<h1 style='color: red;'>🎬 Netflix Customer Insights</h1>", unsafe_allow_html=True)
st.markdown("Predict which customer segment a user belongs to, their churn probability, and get smart recommendations — all based on viewing and account behavior.")

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

# --- Customer Input Form ---
with st.form("customer_form"):
    st.subheader("📝 Enter Customer Details")

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

    submitted = st.form_submit_button("🔍 Predict Segment, Churn & Recommendation")

# --- Prediction logic ---
if submitted:
    user_input = pd.DataFrame([[ 
        age, gender, subscription_type, watch_hours, last_login_days, 
        region, device, payment_method, number_of_profiles, 
        avg_watch_time_per_day, favorite_genre 
    ]], columns=[
        "age", "gender", "subscription_type", "watch_hours", "last_login_days",
        "region", "device", "payment_method", "number_of_profiles",
        "avg_watch_time_per_day", "favorite_genre"
    ])

    try:
        # --- Segment prediction ---
        cluster_label = assign_cluster(user_input)
        insight = cluster_insights.get(cluster_label, {"title": f"Cluster {cluster_label}", "description": "No description available."})
        st.success(f"🎯 Segment: **{insight['title']}**")
        st.info(insight['description'])

        # --- Churn prediction ---
        churn_result = predict_churn(user_input)
        churn_text = "⚠️ Likely to Churn" if churn_result['predicted_class'] == 1 else "✅ Likely to Stay"
        st.success(f"📊 Churn Prediction: **{churn_text}**")
        st.info(f"Churn Probability: {churn_result['churn_probability']}%")

        # --- Recommendation layer ---
        recommendation = recommend_offer(
            cluster_label, 
            churn_result['churn_probability'], 
            subscription_type
        )

        st.markdown("---")
        st.subheader("🎁 Recommended Action")
        st.markdown(f"**{recommendation}**")

    except Exception as e:
        st.error(f"⚠️ Error predicting segment, churn, or recommendation: {e}")
