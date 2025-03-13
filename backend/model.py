import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load dataset
csv_path = os.path.abspath("customer_churn.csv")  
if not os.path.exists(csv_path):
    raise Exception(f"Dataset not found at {csv_path}")

df = pd.read_csv(csv_path)

# Rename columns to lowercase to avoid mismatches
df.rename(columns={"Tenure": "tenure", "Monthly Charges": "monthly_charges", "Total Charges": "total_charges"}, inplace=True)

# Selecting important features
X = df[['tenure', 'monthly_charges', 'total_charges']]
y = df['churn']

# Handle missing values
X = X.fillna(0)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
model_path = os.path.abspath("churn_model.pkl")
joblib.dump(model, model_path)

print(f"✅ Model saved at: {model_path}")
