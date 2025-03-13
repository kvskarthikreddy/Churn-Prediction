import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# ✅ Load data
df = pd.read_csv("data.csv")

# ✅ Prepare Data
X = df[['tenure', 'monthly_charges', 'total_charges']]
y = df['prediction'].map({"Churn": 1, "Not Churn": 0})

# ✅ Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Train New Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ✅ Save Updated Model
joblib.dump(model, "churn_model.pkl")
print("✅ Model Retrained and Saved!")
