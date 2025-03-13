import pandas as pd
import joblib
import schedule
import time
import os
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# ✅ PostgreSQL Database Connection (Update Your Credentials)
DB_URL = "postgresql://customer_churn_db_user:MNMNaERwcaBxxL1XLiknwlNuvwk75jFU@dpg-cv90tr8gph6c73c44st0-a.oregon-postgres.render.com/customer_churn_db"
engine = create_engine(DB_URL)

# ✅ Function to Remove Outliers Using IQR Method
def remove_outliers_iqr(df, columns):
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1  # 🔹 Corrected IQR Calculation
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    return df

# ✅ Function to Retrain ML Model
def retrain_model():
    print("🔄 Retraining Model...")

    # 🔹 Fetch Data from PostgreSQL
    df = pd.read_sql("SELECT * FROM predictions", engine)

    if df.empty:
        print("⚠️ No data found in database. Skipping retraining.")
        return

    # 🔹 Remove Outliers
    df_cleaned = remove_outliers_iqr(df, ["tenure", "monthly_charges", "total_charges"])

    # 🔹 Prepare Data for Training
    X = df_cleaned[['tenure', 'monthly_charges', 'total_charges']]
    y = df_cleaned['prediction']

    # 🔹 Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 🔹 Train New Model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # ✅ Ensure 'models' Directory Exists
    os.makedirs("models", exist_ok=True)

    # 🔹 Save Updated Model in 'models' Folder
    model_path = "models/churn_model.pkl"
    joblib.dump(model, model_path)
    print(f"✅ Model Retrained and Saved at {model_path}")

# ✅ Run Retraining Once for Testing
if __name__ == "__main__":
    retrain_model()

