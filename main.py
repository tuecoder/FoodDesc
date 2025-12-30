from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from services.llm_service import generate_food_description
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Food Description Generator")

# Allow CORS for development convenience (though we are serving static files directly)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoints
@app.post("/generate")
async def generate_description(data: dict):
    food_name = data.get("food_name")
    if not food_name:
        raise HTTPException(status_code=400, detail="Food name is required")
    
    logger.info(f"Generating description for: {food_name}")
    description = await generate_food_description(food_name)
    return {"description": description}

# Mount static files (Frontend)
# This must be mounted after API routes to avoid conflicts if you had a catch-all
app.mount("/", StaticFiles(directory="static", html=True), name="static")
