from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sys
import os

# Add project root to path to allow importing 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.guardian import EthicalGuardian

# --- Pydantic Models for Request/Response ---
class ChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    reasoning_trace: list[str]
    guardian_output: str

# --- FastAPI Application ---
app = FastAPI()
guardian_model = None

# Correctly mount the static directory which is inside 'src'
app.mount("/static", StaticFiles(directory="src/static"), name="static")


@app.on_event("startup")
def load_model():
    """Load the Guardian model once at application startup."""
    global guardian_model
    print("Loading Ethical Guardian v1.0...")
    guardian_model = EthicalGuardian(adapter_path="./models/guardian_v1_adapter", config_path="config.json", prompt_path="prompts.py")
    print("Model loaded successfully.")

@app.get("/", response_class=FileResponse)
async def read_index():
    """Serve the main HTML page from its correct location."""
    return "src/static/index.html"

@app.post("/chat", response_model=ChatResponse)
async def chat_with_guardian(request: ChatRequest):
    """
    Receives a user prompt and returns the Guardian's analysis.
    """
    if not guardian_model:
        return ChatResponse(
            reasoning_trace=["ERROR"],
            guardian_output="Model not loaded. Please check server logs."
        )

    test_case = {"prompt": request.text}
    evaluation = guardian_model.evaluate(test_case)

    return ChatResponse(**evaluation)
