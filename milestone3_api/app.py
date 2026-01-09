from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os

# ---------------- APP ----------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MODEL & VECTORIZER PATH ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "milestone2_models", "random_forest.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "processed_data", "tfidf_vectorizer.pkl")

print("Loading model and vectorizer...")
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)
print("Model and vectorizer loaded successfully.")

# ---------------- REQUEST ----------------
# ---------------- DATABASE ----------------
import database

# Initialize DB on startup
database.init_db()

# ---------------- REQUEST SCHEMAS ----------------
class JobRequest(BaseModel):
    job_description: str

class FlagRequest(BaseModel):
    job_description: str
    prediction: str
    confidence: float
    reason: str

class LoginRequest(BaseModel):
    username: str
    password: str

# ---------------- ROUTES ----------------

@app.post("/login")
def login(data: LoginRequest):
    """Simple Admin Login."""
    if database.verify_user(data.username, data.password):
        return {"success": True, "message": "Login successful"}
    return {"success": False, "message": "Invalid credentials"}

@app.get("/admin/flags")
def get_flags():
    """Get detailed flags for admin table."""
    return database.get_all_flags()

@app.post("/admin/flags/{flag_id}/status")
def update_status(flag_id: int, status: str):
    database.update_flag_status(flag_id, status)
    return {"message": "Status updated"}

@app.delete("/admin/flags/{flag_id}")
def delete_flag(flag_id: int):
    database.delete_flag(flag_id)
    return {"message": "Flag deleted"}

@app.delete("/admin/logs")
def clear_logs():
    database.clear_logs()
    return {"message": "Logs cleared"}

@app.post("/predict")
def predict_job(data: JobRequest):
    text = data.job_description.lower()
    
    result_data = {}
    
    # ---------------- HEURISTIC RULE LAYER ----------------
    # Catch specific local scams that the ML model might miss.
    scam_keywords = [
        "registration fee", "money deposit", "pay regarding", 
        "security deposit", "initial investment", "hidden cost",
        "home-based data processing", "home based data processing",
        "typing job", "without interview", "direct joining",
        "no qualification", "no education", "no experience need"
    ]
    
    # Check for scam keywords, but allow negations (e.g. "NO registration fee")
    heuristic_found = False
    for keyword in scam_keywords:
        if keyword in text:
            if "no " + keyword in text or "without " + keyword in text:
                continue
                
            result_data = {
                "prediction": "Fake Job",
                "confidence": 0.98,
                "reason": f"Detected suspicious term: '{keyword}'"
            }
            heuristic_found = True
            break
            
    if not heuristic_found:
        # ---------------- ML MODEL LAYER ----------------
        vectors = vectorizer.transform([text])
        prediction = model.predict(vectors)[0]
        prob = model.predict_proba(vectors)[0].max()
        result = "Fake Job" if prediction == 1 else "Real Job"
        
        result_data = {
            "prediction": result,
            "confidence": round(float(prob), 2)
        }

    # LOGGING (Milestone 3 Requirement)
    database.log_prediction(data.job_description, result_data["prediction"], result_data["confidence"])
    
    return result_data

@app.post("/flag")
def flag_job(data: FlagRequest):
    """Endpoint for users to flag a post as suspicious/incorrect."""
    database.flag_post(data.job_description, data.prediction, data.confidence, data.reason)
    return {"message": "Thank you! This post has been flagged for review."}

@app.get("/stats")
def get_dashboard_stats():
    """Endpoint for Admin Dashboard (Milestone 4)."""
    return database.get_stats()

