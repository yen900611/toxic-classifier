from fastapi import FastAPI, HTTPException
import joblib
import os
from .schemas import ToxicRequest, ToxicResponse

app = FastAPI(title="Toxic Comment Classifier API")

# 1. Load the Model
# We get the absolute path to ensure we can find the file no matter where we run the command from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "resources", "toxic_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")
except FileNotFoundError:
    print(f"Error: Model not found at {MODEL_PATH}")
    model = None


@app.get("/")
def home():
    return {"message": "Toxic Comment API is running. Go to /docs for the Swagger UI."}


@app.post("/predict", response_model=ToxicResponse)
def predict(request: ToxicRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model is not loaded.")

    # 2. Make Prediction
    # The pipeline handles the vectorization automatically!
    prediction = model.predict([request.text])[0]  # Returns 0 or 1
    probabilities = model.predict_proba([request.text])[0]  # Returns [prob_safe, prob_toxic]

    # 3. Format Response
    # Class 1 is 'toxic', Class 0 is 'clean'
    is_toxic = bool(prediction == 1)
    confidence = float(probabilities[1])  # Probability of being toxic

    return ToxicResponse(is_toxic=is_toxic, confidence=confidence)