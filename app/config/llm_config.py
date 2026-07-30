"""
Centralized LLM Configuration Factory for CrewAI Agents
"""
from crewai import LLM
from app.config.settings import get_settings

def get_llm() -> LLM:
    """Returns a unified CrewAI LLM instance configured for OpenRouter."""
    settings = get_settings()
    return LLM(
        model=settings.LLM_MODEL,
        base_url=settings.LLM_BASE_URL,
        api_key=settings.OPENROUTER_API_KEY,
        temperature=settings.LLM_TEMPERATURE,
        timeout=settings.LLM_TIMEOUT,
    )
