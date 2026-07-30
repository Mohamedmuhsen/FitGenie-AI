"""
FitGenie AI Configuration Settings

Handles environment variables via python-dotenv, API key validation, masking, and server configuration.
"""
import os
import sys
from functools import lru_cache
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file explicitly
load_dotenv(override=True)

# Enforce UTF-8 encoding on Windows standard output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class Settings(BaseSettings):
    """Application settings loaded from environment or .env file."""
    
    # LLM Settings
    LLM_MODEL: str = "openrouter/meta-llama/llama-3.3-70b-instruct"
    LLM_BASE_URL: str = "https://openrouter.ai/api/v1"
    LLM_TEMPERATURE: float = 0.7
    LLM_TIMEOUT: int = 60
    
    # API Keys
    OPENROUTER_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    
    # External API Keys (Placeholders for MVP)
    TAVILY_API_KEY: str = "tvly-placeholder"
    GOOGLE_MAPS_API_KEY: str = "google-maps-placeholder"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def has_valid_api_key(self) -> bool:
        """Check if a genuine OpenRouter or OpenAI API key is present."""
        key = self.OPENROUTER_API_KEY or self.OPENAI_API_KEY
        if not key or len(key) < 15 or key in (
            "sk-or-v1-your-key-here",
            "sk-or-v1-mock-api-key",
            "placeholder"
        ):
            return False
        return True

    def get_masked_api_key(self) -> str:
        """Return masked API key for secure logging without exposing secret."""
        key = self.OPENROUTER_API_KEY or self.OPENAI_API_KEY
        if not key or len(key) < 12:
            return "UNCONFIGURED"
        return f"{key[:12]}...{key[-4:]}"

    def get_api_key_instructions(self) -> dict:
        """Return instructions on how to configure the API key."""
        return {
            "status": "ACTIVE" if self.has_valid_api_key() else "CONFIG_REQUIRED",
            "message": "OpenRouter API Key active and authenticated." if self.has_valid_api_key() else "OpenRouter API Key required.",
            "provider_expected": "OpenRouter (default)",
            "environment_variable": "OPENROUTER_API_KEY",
            "masked_key": self.get_masked_api_key()
        }


@lru_cache()
def get_settings() -> Settings:
    """Singleton getter for app settings."""
    settings = Settings()
    
    # Synchronize environment variables for LiteLLM / CrewAI internal calls
    if settings.OPENROUTER_API_KEY:
        os.environ["OPENROUTER_API_KEY"] = settings.OPENROUTER_API_KEY
    if settings.OPENAI_API_KEY:
        os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
        
    return settings
