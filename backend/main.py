from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import joblib
import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Enable CORS (Frontend <-> Backend Communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to Netlify frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Fetch PostgreSQL Database URL from Environment Variables
DB_URL = os.getenv("DATABASE_URL", "postgresql://customer_churn_db_user:MNMNaERwcaBxxL1XLiknwlNuvwk75jFU@dpg-cv90tr8gph6c73c44st0-a.oregon-postgres.render.com/customer_churn_db")

try:
    engine = create_engine(DB_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    raise Exception(f"❌ Failed to connect to database: {str(e)}")

# ✅ Define Database Table
class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    tenure = Column(Float)
    monthly_charges = Column(Float)
    total_charges = Column(Float)
    prediction = Column(String)

# ✅ Create the database table if it doesn't exist
Base.metadata.create_all(bind=engine)

# ✅ Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Load ML Model
MODEL_PATH = "churn_model.pkl"
if not os.path.exists(MODEL_PATH):
    raise Exception(f"❌ Model file not found! Expected at: {MODEL_PATH}")

model = joblib.load(MODEL_PATH)
print("✅ ML Model Successfully Loaded!")

# ✅ Define Input Data Model
class CustomerData(BaseModel):
    tenure: float
    monthly_charges: float
    total_charges: float

# ✅ Health Check API
@app.get("/")
def home():
    return {"message": "✅ Customer Churn Prediction API is running with PostgreSQL!"}

# ✅ Prediction API
@app.post("/predict/")
def predict(data: CustomerData, db: Session = Depends(get_db)):
    try:
        # Convert input data to Pandas DataFrame
        input_data = pd.DataFrame([[data.tenure, data.monthly_charges, data.total_charges]],
                                  columns=["tenure", "monthly_charges", "total_charges"])

        # Make prediction
        prediction = model.predict(input_data)[0]
        churn_status = "Churn" if prediction == 1 else "Not Churn"

        # Save prediction to PostgreSQL
        new_prediction = Prediction(
            tenure=data.tenure,
            monthly_charges=data.monthly_charges,
            total_charges=data.total_charges,
            prediction=churn_status
        )
        db.add(new_prediction)
        db.commit()

        return {"prediction": churn_status}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error: {str(e)}")







