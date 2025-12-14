from fastapi import FastAPI, HTTPException, Security, Request
from fastapi.security.api_key import APIKeyHeader
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import joblib
import os
from .schemas import ToxicRequest, ToxicResponse

# --- CONFIGURATION ---
# In a real app, these would come from a Database or Environment Variables
VALID_API_KEYS = {"my-secret-key", "frontend-dev-key", "client-123"}
API_KEY_NAME = "X-API-Key"

# --- RATE LIMITER SETUP ---
# key_func=get_remote_address means we limit based on the user's IP address
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Toxic Comment Classifier API")

# Register the Rate Limit Exception Handler so it returns 429 errors cleanly
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- SECURITY SETUP ---
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Dependency that validates the API key exists and is in our approved list.
    """
    if api_key_header in VALID_API_KEYS:
        return api_key_header
    else:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials"
        )


# --- MODEL LOADING ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "resources", "toxic_model.pkl")

pipeline = None
labels = []

try:
    # Load the dictionary we saved in Step 1
    data = joblib.load(MODEL_PATH)
    pipeline = data["pipeline"]
    labels = data["labels"]  # ['toxic', 'severe_toxic', etc...]
    print("Multi-label Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")


# ... (Keep home endpoint) ...

@app.post("/predict", response_model=ToxicResponse)
@limiter.limit("5/minute")
def predict(
        request: Request,
        toxic_req: ToxicRequest,
        api_key: str = Security(get_api_key)
):
    if not pipeline:
        raise HTTPException(status_code=500, detail="Model is not loaded.")

    # MultiOutputClassifier `predict_proba` returns a LIST of arrays
    # One array for each label.
    input_text = [toxic_req.text]
    probs_list = pipeline.predict_proba(input_text)

    results = {}

    # Loop through the 6 labels and extract the probability of "True" (index 1)
    for idx, label in enumerate(labels):
        # probs_list[idx] is the array for the current label
        # [0] gets the first sample (since we only sent one text)
        # [1] gets the probability of class '1' (Positive)
        prob = float(probs_list[idx][0][1])
        results[label] = prob

    return ToxicResponse(results=results)