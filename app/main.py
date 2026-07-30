"""
FitGenie AI - FastAPI Application Entry Point

Exposes API endpoints for:
- / (Web Dashboard UI)
- /api (API Status & Key metadata)
- /health (Health Check)
- /chat (Conversational AI Orchestrator)
- /assessment (Fitness Profile Assessment)
- /workout (Workout Program Generation)
- /nutrition (Nutrition & Meal Planning)
- /supplements (Supplement Protocol)
- /shopping (Gym Gear Recommendations)
- /restaurants (Healthy Dining Discovery)
- /progress (Progress Analytics & Motivation)
"""

import sys
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from app.config.settings import get_settings
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.assessment import AssessmentInput
from app.services.orchestrator_service import OrchestratorService
from app.services.agent_runner import AgentRunner
from app.crews.fitness_crew import FitnessCrew

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fitgenie.main")

# Force UTF-8 on Windows stdout
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle hooks."""
    settings = get_settings()
    masked_key = settings.get_masked_api_key()
    logger.info("=== FitGenie AI Startup ===")
    logger.info(f"  Model: {settings.LLM_MODEL}")
    logger.info(f"  API Key Configured: {settings.has_valid_api_key()} ({masked_key})")
    yield
    logger.info("=== FitGenie AI Shutdown ===")


app = FastAPI(
    title="FitGenie AI",
    description="Multi-Agent AI Fitness Platform built with CrewAI and FastAPI",
    version="0.1.0",
    lifespan=lifespan,
)

# Enable CORS for frontend/mobile apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def serve_ui():
    """Serves the FitGenie AI Web UI."""
    return FileResponse("app/static/index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "FitGenie AI"}


@app.get("/api")
async def api_info():
    """Returns API key status and system metadata."""
    settings = get_settings()
    has_key = settings.has_valid_api_key()
    return {
        "message": "Welcome to FitGenie AI API",
        "version": "0.1.0",
        "status": "active",
        "llm_model": settings.LLM_MODEL,
        "api_key_configured": has_key,
        "instructions": "API key active." if has_key else "Please configure OPENROUTER_API_KEY in .env"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Routes user messages through Orchestrator Service."""
    try:
        orchestrator = OrchestratorService()
        return await orchestrator.process_message(
            message=request.message,
            user_context=request.user_context
        )
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/assessment")
async def run_assessment(input_data: AssessmentInput):
    """Fitness Assessment endpoint."""
    try:
        payload = input_data.model_dump()
        crew = FitnessCrew.assessment_crew(payload)
        return await AgentRunner.execute_crew_async("assessment", crew, payload)
    except Exception as e:
        logger.error(f"Assessment error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/workout")
async def create_workout(input_data: dict):
    """Workout Planning endpoint."""
    try:
        assessment_data = input_data.get("assessment", input_data)
        crew = FitnessCrew.workout_crew(assessment_data)
        return await AgentRunner.execute_crew_async("workout", crew, assessment_data)
    except Exception as e:
        logger.error(f"Workout error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/nutrition")
async def create_nutrition(input_data: dict):
    """Nutrition Planning endpoint."""
    try:
        assessment_data = input_data.get("assessment", input_data)
        crew = FitnessCrew.nutrition_crew(assessment_data)
        return await AgentRunner.execute_crew_async("nutrition", crew, assessment_data)
    except Exception as e:
        logger.error(f"Nutrition error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/supplements")
async def create_supplements(input_data: dict):
    """Supplement Recommendation endpoint."""
    try:
        assessment_data = input_data.get("assessment", input_data)
        crew = FitnessCrew.supplement_crew(assessment_data)
        return await AgentRunner.execute_crew_async("supplements", crew, assessment_data)
    except Exception as e:
        logger.error(f"Supplements error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/shopping")
async def create_shopping(input_data: dict):
    """Gym Shopping Recommendation endpoint."""
    try:
        crew = FitnessCrew.shopping_crew(input_data)
        return await AgentRunner.execute_crew_async("shopping", crew, input_data)
    except Exception as e:
        logger.error(f"Shopping error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/restaurants")
async def find_restaurants(input_data: dict):
    """Healthy Restaurant Recommendation endpoint."""
    try:
        crew = FitnessCrew.restaurant_crew(input_data)
        return await AgentRunner.execute_crew_async("restaurants", crew, input_data)
    except Exception as e:
        logger.error(f"Restaurants error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/progress")
async def track_progress(input_data: dict):
    """Progress Tracking & Analytics endpoint."""
    try:
        crew = FitnessCrew.progress_crew(input_data)
        return await AgentRunner.execute_crew_async("progress", crew, input_data)
    except Exception as e:
        logger.error(f"Progress error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
