import pandas as pd
import joblib
import json

# Load GBM model and features
gb_model = joblib.load("models/gb_churn_model.joblib")
with open("models/gb_features.json", "r") as f:
    gb_features = json.load(f)

def preprocess_churn(df: pd.DataFrame) -> pd.DataFrame:
    # Feature engineering
    df['avg_watch_time_per_profile'] = df['avg_watch_time_per_day'] / df['number_of_profiles']
    mapping = {"Basic": 8.99, "Standard": 13.99, "Premium": 17.99}
    df['subscription_price'] = df['subscription_type'].map(mapping)

    # One-hot encode categorical features
    df = pd.get_dummies(df, columns=['payment_method','region','device','favorite_genre'], drop_first=True)

    # Drop redundant columns
    drop_cols = ['age','gender','subscription_type']
    df = df.drop(columns=[col for col in drop_cols if col in df.columns], errors='ignore')

    # Ensure same column order as training
    for col in gb_features:
        if col not in df.columns:
            df[col] = 0
    df = df[gb_features]

    return df

def predict_churn(user_df: pd.DataFrame) -> dict:
    X_proc = preprocess_churn(user_df)
    pred = gb_model.predict(X_proc)[0]
    prob = gb_model.predict_proba(X_proc)[0][1]
    return {
        "predicted_class": int(pred),
        "churn_probability": round(prob*100,2)
    }
