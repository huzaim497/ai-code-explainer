import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.ai_service import explain_code


# Create FastAPI application
app = FastAPI(
    title="AI Code Explainer API",
    description="AI-based source code explanation backend",
    version="1.0.0"
)


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define the structure of incoming requests
class ExplainRequest(BaseModel):
    code: str
    language: str
    level: str


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "running",
        "message": "AI Code Explainer backend is working"
    }


# Main code explanation endpoint
@app.post("/api/explain")
def explain(request: ExplainRequest):

    # Validate source code
    if not request.code.strip():
        raise HTTPException(
            status_code=400,
            detail="Source code cannot be empty."
        )

    if len(request.code) > 15000:
        raise HTTPException(
            status_code=400,
            detail="Source code is too long. Please reduce its length."
        )

    # Validate programming language
    allowed_languages = [
        "Python", "Java", "JavaScript", "C", "C++"
    ]

    if request.language not in allowed_languages:
        raise HTTPException(
            status_code=400,
            detail="Unsupported programming language."
        )

    # Validate explanation level
    if request.level not in ["Beginner", "Advanced"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid explanation level."
        )

    try:
        result = explain_code(
            code=request.code,
            language=request.language,
            level=request.level
        )

        return result

except Exception as error:
    traceback.print_exc()
    raise HTTPException(
        status_code=500,
        detail=f"AI explanation failed: {str(error)}"
    )