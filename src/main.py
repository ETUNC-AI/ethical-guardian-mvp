from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from fastapi.staticfiles import StaticFiles # <-- THIS IS THE MISSING LINE I ADDED
from starlette.responses import FileResponse

# (The rest of the file content remains the same as it was, 
# this just ensures the import is correctly placed)

from guardian import EthicalGuardian

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestCase(BaseModel):
    prompt: str

guardian_model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model during startup
    global guardian_model
    logger.info("Loading Ethical Guardian model...")
    try:
        # NOTE: Update paths as needed for your environment
        guardian_model = EthicalGuardian(
            adapter_path="./models/guardian_v1_adapter", 
            config_path="config.json", 
            prompt_path="prompts.py"
        )
        logger.info("Ethical Guardian model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        guardian_model = None # Ensure model is None if loading fails
    yield
    # Clean up resources if needed
    logger.info("Application shutdown.")

app = FastAPI(lifespan=lifespan)

# Mount the static directory to serve index.html, css, js
app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse('src/static/index.html')

@app.post("/evaluate")
async def evaluate_prompt(test_case: TestCase):
    if guardian_model is None:
        raise HTTPException(status_code=503, detail="Model is not available or failed to load.")

    try:
        logger.info(f"Received prompt for evaluation: {test_case.prompt}")
        result = guardian_model.evaluate(test_case.dict())
        logger.info("Evaluation successful.")
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"An error occurred during evaluation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")
