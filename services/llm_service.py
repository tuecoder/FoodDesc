import httpx
import logging

# Configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "gemma3" # You can change this to 'mistral' or whatever you have pulled

logger = logging.getLogger(__name__)

async def generate_food_description(food_name: str) -> str:
    """
    Generates a short and catchy description for a given food name using a local LLM.
    """
    prompt = f"Write a short, catchy, mouth-watering description for {food_name}. Keep it under 50 words. Do not include quotes."
    
    payload = {
        "model": DEFAULT_MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OLLAMA_API_URL, json=payload, timeout=30.0)
            if response.status_code != 200:
                error_msg = response.text
                logger.error(f"Ollama API Error: {response.status_code} - {error_msg}")
                return f"Error: Ollama returned {response.status_code}. Message: {error_msg}"
            
            data = response.json()
            return data.get("response", "Error: No response generated.")
    except httpx.RequestError as e:
        logger.error(f"Error connecting to Ollama: {e}")
        return f"Error: Could not connect to local LLM. Is Ollama running? Details: {e}"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return f"Error: Something went wrong. {e}"
