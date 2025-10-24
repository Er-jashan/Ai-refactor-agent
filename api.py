import uvicorn
import os
import time
from typing import Dict, Any

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse # Imported for explicit JSON response
from fastapi.middleware.cors import CORSMiddleware # Imported for CORS fix
from google import genai
from google.genai import types
from google.genai.errors import APIError

# --- 1. Initialize FastAPI App and CORS Middleware ---
app = FastAPI(title="AI Refactoring Agent API")

# FIX: Add CORS middleware to allow the browser frontend to communicate with the local server.
# This is crucial when the frontend and backend are running on different ports/origins.
origins = ["*"] # Allow all origins for development purposes

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- 2. Initialization and Configuration ---
client = None
LLM_MODEL = 'gemini-2.5-flash'
IS_MOCK_MODE = False

# Get the API key from the environment variable
api_key = os.getenv("GEMINI_API_KEY")

try:
    if api_key:
        # Initialize the client with the retrieved API key
        client = genai.Client(api_key=api_key)
        print("Gemini client initialized successfully. Real AI calls will be made.")
    else:
        # If no key is found, run in mock mode
        IS_MOCK_MODE = True
        print("--- WARNING: GEMINI_API_KEY not found. RUNNING IN MOCK MODE. ---")

except Exception as e:
    IS_MOCK_MODE = True
    print(f"Warning: Failed to initialize Gemini client. Running in MOCK MODE. Error: {e}")


# --- 3. API Endpoint ---

@app.post("/refactor")
async def refactor_code(
    user_code: str = Form(...),
    refactor_request: str = Form(...)
) -> Dict[str, Any]:
    """
    Takes user code and a refactoring request, sends it to the LLM, and 
    returns the suggested refactored code (or a mock response).
    """
    
    # --- MOCK MODE HANDLING ---
    if IS_MOCK_MODE:
        mock_response = (
            f"// MOCK RESPONSE: LLM Service Unavailable or Key Error.\n"
            f"// Request: '{refactor_request}'\n\n"
            f"```python\n"
            f"def refactor_success(original_code):\n"
            f"    # This is placeholder code to test the UI/UX flow.\n"
            f"    # Request: {refactor_request}\n"
            f"    # Original: {user_code.splitlines()[0][:40]}...\n"
            f"    return 'Mock Refactoring Complete!'\n"
            f"```"
        )
        # Simulate a network delay for better UI testing
        time.sleep(1) 
        print("Returning mock response.")
        # Ensure the response format is explicit and correct for the frontend
        return JSONResponse(
            content={"success": True, "refactored_code": mock_response},
            status_code=200
        )

    # --- REAL AI MODE HANDLING ---
    
    # 4. Construct System Instruction (This defines the Agent's Role)
    system_prompt = (
        "You are a world-class code refactoring agent specializing in performance, "
        "security, and modern language practices. Your task is to take the "
        "user's provided code and their refactoring request, and return ONLY the "
        "COMPLETE, MODIFIED code block inside a single Markdown code block. "
        "Do not add any extra text, explanations, or filler outside the code block. "
        "Maintain the original programming language (e.g., Python, JavaScript, Java)."
    )

    # 5. Construct User Prompt
    user_prompt = (
        f"Refactoring Request: {refactor_request}\n\n"
        f"The user wants you to modify the following code:\n\n---\n{user_code}\n---"
    )

    try:
        # 6. Call the Gemini API
        print(f"Calling {LLM_MODEL} with request: '{refactor_request[:50]}...'")
        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=[user_prompt],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt
            )
        )

        # 7. Extract the generated text
        refactored_code = response.text.strip()
        
        # Ensure the response is always explicitly JSON and contains the required keys
        return JSONResponse(
            content={"success": True, "refactored_code": refactored_code},
            status_code=200
        )

    except APIError as e:
        print(f"Gemini API Error: {e}")
        # Raise an HTTP exception for client to handle
        raise HTTPException(
            status_code=500, 
            detail=f"AI Service Error: Failed to process request due to API error. Details: {e}"
        )
    except Exception as e:
        print(f"Unexpected Error: {e}")
        # Raise a general exception for client to handle
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected server error occurred: {e}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
