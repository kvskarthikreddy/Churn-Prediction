import pandas as pd
from sqlalchemy import create_engine
import os

# ✅ Connect to PostgreSQL
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

# ✅ Fetch past predictions
df = pd.read_sql("SELECT * FROM predictions", engine)

# ✅ Save for retraining
df.to_csv("data.csv", index=False)
print("✅ Data fetched and saved!")
