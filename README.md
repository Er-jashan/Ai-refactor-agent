#AI Refactoring Agent

The AI Refactoring Agent is a full-stack web application designed to help developers quickly and securely refactor their code using Google's powerful Gemini 2.5 Flash model. Users provide existing code and a natural language request (e.g., "Make this secure and use f-strings in Python"), and the FastAPI backend sends the request to the AI, returning the clean, refactored code directly to the browser.

This project uses a decoupled architecture for deployment, with a Python backend handling the AI logic and an HTML file serving the user interface.

✨ Features

Intelligent Refactoring: Leverages Gemini 2.5 Flash for high-quality, contextual code refactoring based on natural language instructions.

Secure Backend: FastAPI server acts as a secure proxy for the Gemini API key, preventing exposure in the frontend.

Universal Input: Supports refactoring logic across multiple programming languages (Python, JavaScript, etc.).

Modern Interface: Uses a single-page HTML application with the Monaco Editor (the editor used in VS Code) for a professional, syntax-highlighted code editing experience.

Production Ready: Configured with CORS and a structure ready for cloud deployment (e.g., Render).

#🏛️ Architecture & Project Structure

The application is split into a Python backend and a single static frontend file.

Ai-refactor-agent/
├── api.py              # FastAPI server, AI logic, and API endpoint (`/refactor`).
├── requirements.txt    # Python dependencies for FastAPI and google-genai.
└── frontend/
    └── index.html      # Single-page HTML frontend (UI, Monaco Editor, JS logic).


#🛠️ Local Setup (Development)

To run this application locally, you need Python (3.9+) and to set your Gemini API key.

Clone the Repository:

git clone [https://github.com/Er-jashan/Ai-refactor-agent.git](https://github.com/Er-jashan/Ai-refactor-agent.git)
cd Ai-refactor-agent


Install Dependencies:

pip install -r requirements.txt


Set Environment Variable:
Your application requires the GEMINI_API_KEY to be set. Note: In the provided api.py (the latest working version), a fallback key is temporarily used to ensure local testing works, but for security, you should set your own key.

Linux/macOS:

export GEMINI_API_KEY="YOUR_API_KEY"


Windows PowerShell:

$env:GEMINI_API_KEY = "YOUR_API_KEY"


Run the Backend Server:

python -m uvicorn api:app


The server will start at http://127.0.0.1:8000.

Access the Frontend:
Open the static/index.html file directly in your web browser. The JavaScript will automatically connect to the running FastAPI server for the API calls.

#🚀 Deployment Strategy (Production)

This project is structured for deployment as a single Web Service on platforms like Render or Google Cloud Run, where the FastAPI server handles both the API logic and the serving of the static HTML/JS frontend.

Configuration Steps (Example: Render)

Connect Git: Connect your GitHub repository to your Render account.

Service Type: Create a Web Service.

Build Command:

pip install -r requirements.txt



Start Command:

uvicorn api:app --host 0.0.0.0 --port $PORT

//Project Preview :-
https://ai-refactor-agent.netlify.app/

Note:- It will take upto 1 min to respond, because site may go to sleep.

YOU-TUBE VIDEO LINK :-
https://youtu.be/h0upM0Bm8dc


