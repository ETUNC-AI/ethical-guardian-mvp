from fastapi import FastAPI
from pydantic import BaseModel
from src.guardian import EthicalGuardian

app = FastAPI(title="Ethical Guardian API")
guardian_model = None

class ChatRequest(BaseModel):
    text: str
class ChatResponse(BaseModel):
    reasoning_trace: list[str]
    guardian_output: str

@app.on_event("startup")
def load_model():
    global guardian_model
    print("Loading Ethical Guardian v1.0...")
    guardian_model = EthicalGuardian(
        adapter_path="./models/guardian_v1_adapter",
        config_path="config.json",
        prompt_path="prompts.py"
    )
    print("Model loaded successfully.")

@app.post("/chat", response_model=ChatResponse)
async def chat_with_guardian(request: ChatRequest):
    test_case = {"prompt": request.text}
    evaluation = guardian_model.evaluate(test_case)
    return ChatResponse(**evaluation)
