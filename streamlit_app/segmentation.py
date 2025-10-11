import pandas as pd
import numpy as np
import joblib
import json
import os

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")  # adjust if needed

# --- Load saved models and files ---
kmeans_model = joblib.load(os.path.join(MODEL_DIR, "kmeans_segmentation_model.joblib"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.joblib"))
encoder = joblib.load(os.path.join(MODEL_DIR, "encoder.joblib"))
pca = joblib.load(os.path.join(MODEL_DIR, "pca.joblib"))

with open(os.path.join(MODEL_DIR, "kmeans_features.json"), "r") as f:
    expected_features = json.load(f)

# --- Preprocessing function ---
def preprocess_input(df: pd.DataFrame) -> np.ndarray:
    """Preprocess input dataframe to match training features and apply PCA."""

    # Feature engineering
    df['watch_hours_per_profile'] = df['watch_hours'] / df['number_of_profiles'].replace(0, 1)

    # Numeric columns
    numeric_cols = ['age', 'watch_hours', 'last_login_days', 'number_of_profiles', 
                    'avg_watch_time_per_day', 'watch_hours_per_profile']
    df_num_scaled = scaler.transform(df[numeric_cols])

    # Categorical columns
    categorical_cols = ['subscription_type', 'device', 'gender', 'favorite_genre', 'payment_method', 'region']

    # Handle unknown categories by ignoring them
    df_cat_encoded = encoder.transform(df[categorical_cols].apply(lambda x: x.where(x.isin(encoder.categories_[categorical_cols.index(x.name)]), 'Other')))

    # Combine numeric and categorical features
    X_combined = np.hstack([df_num_scaled, df_cat_encoded])

    # Apply PCA
    X_pca = pca.transform(X_combined)

    return X_pca


# --- Cluster prediction ---
def assign_cluster(df: pd.DataFrame) -> int:
    """Predict KMeans cluster for a new user."""
    processed_data = preprocess_input(df)
    cluster = kmeans_model.predict(processed_data)
    return int(cluster[0])
