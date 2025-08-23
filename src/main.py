from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# This allows Python to find the 'guardian' module in the parent 'src' directory
# No changes needed here, but it's important for context.

from guardian import EthicalGuardian

# --- Pydantic Models for Request/Response ---
class ChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    reasoning_trace: list[str]
    guardian_output: str

# --- FastAPI Application ---
app = FastAPI()
guardian_model = None

@app.on_event("startup")
def load_model():
    """Load the Guardian model once at application startup."""
    global guardian_model
    print("Loading Ethical Guardian v1.0...")
    guardian_model = EthicalGuardian(adapter_path="../models/guardian_v1_adapter")
    print("Model loaded successfully.")

@app.get("/")
def read_root():
    return {"message": "Ethical Guardian API is running."}

@app.post("/chat", response_model=ChatResponse)
async def chat_with_guardian(request: ChatRequest):
    """
    Receives a user prompt and returns the Guardian's analysis.
    """
    if not guardian_model:
        # This is an error condition, so we need to return a valid ChatResponse
        return ChatResponse(
            reasoning_trace=["ERROR"],
            guardian_output="Model not loaded. Please check server logs."
        )

    # Format the request for the model
    test_case = {"prompt": request.text}
    evaluation = guardian_model.evaluate(test_case)

    return ChatResponse(**evaluation)
