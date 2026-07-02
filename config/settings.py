"""
Configuration management for the AI Assistant.
Loads settings from environment variables with sensible defaults.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings from environment variables."""

    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent
    LOGS_DIR = PROJECT_ROOT / "logs"
    DATA_DIR = PROJECT_ROOT / "data"

    # Ensure directories exist
    LOGS_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)

    # LLM Provider Configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    OPENAI_BASE_URL: Optional[str] = os.getenv("OPENAI_BASE_URL", None)
    
    # Anthropic Claude
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")
    
    # HuggingFace
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    HUGGINGFACE_MODEL: str = os.getenv("HUGGINGFACE_MODEL", "meta-llama/Llama-2-7b-chat")
    
    # Ollama (local LLM)
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama2")

    # Assistant Configuration
    ASSISTANT_NAME: str = os.getenv("ASSISTANT_NAME", "PersonalAssistant")
    ASSISTANT_DESCRIPTION: str = os.getenv("ASSISTANT_DESCRIPTION", "Your personal AI assistant")
    MAX_MEMORY_MESSAGES: int = int(os.getenv("MAX_MEMORY_MESSAGES", "50"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2000"))
    TOP_P: float = float(os.getenv("TOP_P", "1.0"))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", str(LOGS_DIR / "assistant.log"))
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Crypto Data APIs (Optional)
    CRYPTOCOMPARE_API_KEY: Optional[str] = os.getenv("CRYPTOCOMPARE_API_KEY", None)
    COINGECKO_API_KEY: Optional[str] = os.getenv("COINGECKO_API_KEY", None)

    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///assistant_db.sqlite")

    # Security Settings
    SECURE_MODE: bool = os.getenv("SECURE_MODE", "true").lower() == "true"
    ENABLE_RATE_LIMITING: bool = os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"
    RATE_LIMIT_CALLS: int = int(os.getenv("RATE_LIMIT_CALLS", "100"))
    RATE_LIMIT_PERIOD: int = int(os.getenv("RATE_LIMIT_PERIOD", "60"))

    # Feature Flags
    ENABLE_MEMORY: bool = os.getenv("ENABLE_MEMORY", "true").lower() == "true"
    ENABLE_TOOLS: bool = os.getenv("ENABLE_TOOLS", "true").lower() == "true"
    ENABLE_STREAMING: bool = os.getenv("ENABLE_STREAMING", "false").lower() == "true"

    @classmethod
    def validate(cls) -> None:
        """Validate critical settings."""
        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        if cls.LLM_PROVIDER == "claude" and not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is required when LLM_PROVIDER=claude")
        if cls.TEMPERATURE < 0 or cls.TEMPERATURE > 2:
            raise ValueError("TEMPERATURE must be between 0 and 2")
        if cls.TOP_P < 0 or cls.TOP_P > 1:
            raise ValueError("TOP_P must be between 0 and 1")

    @classmethod
    def get_provider_config(cls) -> dict:
        """Get configuration for the selected LLM provider."""
        configs = {
            "openai": {
                "api_key": cls.OPENAI_API_KEY,
                "model": cls.OPENAI_MODEL,
                "base_url": cls.OPENAI_BASE_URL,
            },
            "claude": {
                "api_key": cls.ANTHROPIC_API_KEY,
                "model": cls.CLAUDE_MODEL,
            },
            "huggingface": {
                "api_key": cls.HUGGINGFACE_API_KEY,
                "model": cls.HUGGINGFACE_MODEL,
            },
            "ollama": {
                "base_url": cls.OLLAMA_BASE_URL,
                "model": cls.OLLAMA_MODEL,
            },
        }
        return configs.get(cls.LLM_PROVIDER, {})


# Create a global settings instance
settings = Settings()
