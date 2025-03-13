import pandas as pd
import numpy as np

np.random.seed(42)
data = {
    "customer_id": range(1, 1001),
    "tenure": np.random.randint(1, 72, 1000),
    "monthly_charges": np.round(np.random.uniform(20, 150, 1000), 2),
    "total_charges": np.round(np.random.uniform(50, 10000, 1000), 2),
    "churn": np.random.choice([0, 1], 1000, p=[0.75, 0.25])  # 25% churn rate
}

df = pd.DataFrame(data)
df["total_charges"] = df["total_charges"].replace("", np.nan).fillna(df["total_charges"].median())
df.to_csv("backend/customer_churn.csv", index=False)
print("Dataset fixed: backend/customer_churn.csv")

