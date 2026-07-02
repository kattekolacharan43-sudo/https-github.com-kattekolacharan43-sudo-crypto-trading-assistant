"""
Input validation utilities for the AI Assistant.
"""

from typing import Any, Optional
import re


class InputValidator:
    """Validate user inputs and data."""

    @staticmethod
    def validate_string(
        value: Any,
        min_length: int = 1,
        max_length: int = 10000,
        allow_empty: bool = False,
    ) -> bool:
        """
        Validate string input.

        Args:
            value: Input to validate
            min_length: Minimum string length
            max_length: Maximum string length
            allow_empty: Allow empty strings

        Returns:
            True if valid, False otherwise
        """
        if not isinstance(value, str):
            return False
        if not allow_empty and not value.strip():
            return False
        return min_length <= len(value) <= max_length

    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validate API key format.

        Args:
            api_key: API key to validate

        Returns:
            True if valid format, False otherwise
        """
        if not isinstance(api_key, str):
            return False
        if len(api_key) < 10:
            return False
        return True

    @staticmethod
    def validate_temperature(temperature: float) -> bool:
        """
        Validate temperature value.

        Args:
            temperature: Temperature value (0-2)

        Returns:
            True if valid, False otherwise
        """
        return isinstance(temperature, (int, float)) and 0 <= temperature <= 2

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.

        Args:
            email: Email to validate

        Returns:
            True if valid email format, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return isinstance(email, str) and bool(re.match(pattern, email))

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL format.

        Args:
            url: URL to validate

        Returns:
            True if valid URL format, False otherwise
        """
        pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
        return isinstance(url, str) and bool(re.match(pattern, url))

    @staticmethod
    def sanitize_input(input_text: str, max_length: int = 10000) -> str:
        """
        Sanitize user input to prevent injection attacks.

        Args:
            input_text: Input to sanitize
            max_length: Maximum allowed length

        Returns:
            Sanitized input
        """
        if not isinstance(input_text, str):
            return ""
        
        # Remove control characters
        sanitized = ''.join(char for char in input_text if ord(char) >= 32 or char in '\n\t\r')
        
        # Limit length
        sanitized = sanitized[:max_length]
        
        # Remove leading/trailing whitespace
        sanitized = sanitized.strip()
        
        return sanitized

    @staticmethod
    def validate_dict_keys(
        data: dict,
        required_keys: list,
        optional_keys: Optional[list] = None,
    ) -> bool:
        """
        Validate dictionary has required and optional keys.

        Args:
            data: Dictionary to validate
            required_keys: List of required keys
            optional_keys: List of optional keys

        Returns:
            True if valid, False otherwise
        """
        if not isinstance(data, dict):
            return False
        
        # Check required keys
        if not all(key in data for key in required_keys):
            return False
        
        # Check for unexpected keys
        allowed_keys = set(required_keys)
        if optional_keys:
            allowed_keys.update(optional_keys)
        
        return all(key in allowed_keys for key in data.keys())
