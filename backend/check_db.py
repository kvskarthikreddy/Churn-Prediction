from sqlalchemy import create_engine
import pandas as pd

# ✅ Database URL (Replace if needed)
DB_URL = "postgresql://customer_churn_db_user:MNMNaERwcaBxxL1XLiknwlNuvwk75jFU@dpg-cv90tr8gph6c73c44st0-a.oregon-postgres.render.com/customer_churn_db"

# ✅ Create a database connection
engine = create_engine(DB_URL)

# ✅ Read the predictions table
query = "SELECT * FROM predictions;"
df = pd.read_sql(query, engine)

# ✅ Print the stored data
print(df)
