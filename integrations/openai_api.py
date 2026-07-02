"""
OpenAI API integration for the AI Assistant.
Supports GPT-3.5, GPT-4, and other OpenAI models.
"""

from typing import Optional, List, Dict, Any
import openai
from openai import OpenAI, APIError, APIConnectionError, RateLimitError
from integrations.llm_provider import LLMProvider, LLMResponse
from utils.logger import get_logger

logger = get_logger(__name__)


class OpenAIProvider(LLMProvider):
    """OpenAI API provider implementation."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4-turbo-preview",
        base_url: Optional[str] = None,
    ):
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key
            model: Model name (default: gpt-4-turbo-preview)
            base_url: Optional custom base URL
        """
        super().__init__(api_key, model)
        
        # Initialize client
        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=api_key)
        
        logger.info(f"OpenAI provider initialized with model: {model}")

    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        **kwargs,
    ) -> LLMResponse:
        """
        Generate a response using OpenAI API.

        Args:
            messages: List of message dictionaries
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            top_p: Top-p sampling parameter
            frequency_penalty: Frequency penalty (-2 to 2)
            presence_penalty: Presence penalty (-2 to 2)
            **kwargs: Additional parameters

        Returns:
            LLMResponse object

        Raises:
            APIError: If API call fails
            RateLimitError: If rate limited
            APIConnectionError: If connection fails
        """
        try:
            logger.debug(f"Generating response with {len(messages)} messages")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                **kwargs,
            )

            logger.debug(f"OpenAI API call successful. Finish reason: {response.choices[0].finish_reason}")

            return LLMResponse(
                content=response.choices[0].message.content,
                model=response.model,
                finish_reason=response.choices[0].finish_reason,
                usage={
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens,
                },
                metadata={
                    'created': response.created,
                    'id': response.id,
                },
            )

        except RateLimitError as e:
            logger.error(f"OpenAI rate limit error: {str(e)}")
            raise
        except APIConnectionError as e:
            logger.error(f"OpenAI connection error: {str(e)}")
            raise
        except APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise

    def validate_connection(self) -> bool:
        """
        Validate OpenAI API connection.

        Returns:
            True if connection is valid
        """
        try:
            response = self.client.models.retrieve(self.model)
            logger.info(f"OpenAI connection validated for model: {self.model}")
            return True
        except Exception as e:
            logger.error(f"OpenAI connection validation failed: {str(e)}")
            return False

    def list_models(self) -> List[str]:
        """
        List available OpenAI models.

        Returns:
            List of model names
        """
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            logger.error(f"Failed to list models: {str(e)}")
            return []

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model.

        Returns:
            Dictionary with model information
        """
        info = super().get_model_info()
        try:
            model = self.client.models.retrieve(self.model)
            info.update({
                'created': model.created,
                'owned_by': model.owned_by,
            })
        except Exception as e:
            logger.warning(f"Could not retrieve model info: {str(e)}")
        
        return info
