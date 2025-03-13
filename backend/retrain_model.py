import os
import pandas as pd
import joblib
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# ✅ PostgreSQL Database Connection (Update Your Credentials)
DB_URL = "postgresql://customer_churn_db_user:MNMNaERwcaBxxL1XLiknwlNuvwk75jFU@dpg-cv90tr8gph6c73c44st0-a.oregon-postgres.render.com/customer_churn_db"
engine = create_engine(DB_URL)

# ✅ Function to Remove Outliers (IQR Method)
def remove_outliers_iqr(df, columns):
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    return df

# ✅ Function to Retrain ML Model
def retrain_model():
    print("🔄 Retraining Model...")

    # 🔹 Fetch Data from PostgreSQL
    try:
        df = pd.read_sql("SELECT tenure, monthly_charges, total_charges, prediction FROM predictions", engine)
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return

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

    # 🔹 Save Updated Model
    joblib.dump(model, "backend/churn_model.pkl")  # ✅ Save inside `backend`
    print("✅ Model Retrained and Saved!")

# ✅ Run Retraining
if __name__ == "__main__":
    retrain_model()
