"""
Abstract LLM provider interface for extensibility.
Supports multiple LLM backends (OpenAI, Claude, HuggingFace, Ollama).
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)


class LLMResponse:
    """Represents a response from an LLM."""

    def __init__(
        self,
        content: str,
        model: str,
        finish_reason: str = "stop",
        usage: Optional[Dict[str, int]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize LLM response.

        Args:
            content: Response content
            model: Model name
            finish_reason: Why the model stopped
            usage: Token usage information
            metadata: Additional metadata
        """
        self.content = content
        self.model = model
        self.finish_reason = finish_reason
        self.usage = usage or {}
        self.metadata = metadata or {}

    def __str__(self) -> str:
        """String representation."""
        return self.content

    def __repr__(self) -> str:
        """Detailed representation."""
        return (
            f"LLMResponse(model={self.model}, "
            f"finish_reason={self.finish_reason}, "
            f"content_length={len(self.content)})"
        )


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, api_key: str, model: str):
        """
        Initialize LLM provider.

        Args:
            api_key: API key for the provider
            model: Model name to use
        """
        self.api_key = api_key
        self.model = model
        logger.debug(f"{self.__class__.__name__} initialized with model: {model}")

    @abstractmethod
    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> LLMResponse:
        """
        Generate a response from the LLM.

        Args:
            messages: List of message dictionaries (role, content)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Provider-specific parameters

        Returns:
            LLMResponse object
        """
        pass

    @abstractmethod
    def validate_connection(self) -> bool:
        """
        Validate that the provider can be accessed.

        Returns:
            True if connection is valid
        """
        pass

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model.

        Returns:
            Dictionary with model information
        """
        return {
            'model': self.model,
            'provider': self.__class__.__name__,
        }
