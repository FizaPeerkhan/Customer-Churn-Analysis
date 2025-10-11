# prediction.py
import pandas as pd
import joblib
import json

# Load GBM model and features
gb_model = joblib.load("models/gb_churn_model.joblib")
with open("models/gb_features.json", "r") as f:
    gb_features = json.load(f)

def preprocess_churn(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess user input to match model features.
    Includes feature engineering, one-hot encoding, and column alignment.
    """
    # Feature engineering
    df['avg_watch_time_per_profile'] = df['avg_watch_time_per_day'] / df['number_of_profiles']
    subscription_price_map = {"Basic": 8.99, "Standard": 13.99, "Premium": 17.99}
    df['subscription_price'] = df['subscription_type'].map(subscription_price_map)

    # One-hot encode categorical features
    df = pd.get_dummies(df, columns=['payment_method','region','device','favorite_genre'], drop_first=True)

    # Drop redundant columns
    drop_cols = ['age','gender','subscription_type']
    df = df.drop(columns=[col for col in drop_cols if col in df.columns], errors='ignore')

    # Ensure same column order as model training
    for col in gb_features:
        if col not in df.columns:
            df[col] = 0
    df = df[gb_features]

    return df

def predict_churn(user_df: pd.DataFrame) -> dict:
    """
    Predict churn class and probability.
    Returns a dictionary: {'predicted_class': 0/1, 'churn_probability': float}
    """
    X_proc = preprocess_churn(user_df)
    pred_class = gb_model.predict(X_proc)[0]
    pred_prob = gb_model.predict_proba(X_proc)[0][1]

    return {
        "predicted_class": int(pred_class),
        "churn_probability": round(pred_prob*100, 2)
    }

# Example usage
if __name__ == "__main__":
    sample_user = pd.DataFrame([{
        "age": 30,
        "gender": "Female",
        "region": "Asia",
        "number_of_profiles": 2,
        "subscription_type": "Basic",
        "device": "Mobile",
        "payment_method": "Credit Card",
        "watch_hours": 50,
        "avg_watch_time_per_day": 2.5,
        "last_login_days": 5,
        "favorite_genre": "Drama"
    }])

    result = predict_churn(sample_user)
    print("Churn Prediction:", result)
