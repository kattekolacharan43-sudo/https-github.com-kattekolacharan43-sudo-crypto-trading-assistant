"""
Main AI Assistant class.
Orchestrates LLM interactions with memory, tools, and context management.
"""

from typing import Optional, List, Dict, Any
from core.memory import ConversationMemory
from core.tools import ToolRegistry, get_tool_registry
from integrations.llm_provider import LLMProvider, LLMResponse
from integrations.openai_api import OpenAIProvider
from config.settings import settings
from utils.logger import get_logger
from utils.validators import InputValidator

logger = get_logger(__name__)


class PersonalAssistant:
    """Main AI Assistant orchestrator."""

    def __init__(
        self,
        name: Optional[str] = None,
        llm_provider: Optional[LLMProvider] = None,
        enable_memory: bool = True,
        enable_tools: bool = True,
        system_prompt: Optional[str] = None,
    ):
        """
        Initialize the Personal Assistant.

        Args:
            name: Assistant name
            llm_provider: LLM provider instance (defaults to OpenAI)
            enable_memory: Enable conversation memory
            enable_tools: Enable tool execution
            system_prompt: Custom system prompt
        """
        self.name = name or settings.ASSISTANT_NAME
        self.enable_memory = enable_memory
        self.enable_tools = enable_tools

        # Initialize LLM provider
        if llm_provider is None:
            self._initialize_default_provider()
        else:
            self.llm_provider = llm_provider

        # Initialize memory
        self.memory = (
            ConversationMemory(max_messages=settings.MAX_MEMORY_MESSAGES)
            if enable_memory
            else None
        )

        # Initialize tools
        self.tools = get_tool_registry() if enable_tools else None

        # System prompt
        self.system_prompt = system_prompt or self._get_default_system_prompt()

        logger.info(f"PersonalAssistant '{self.name}' initialized")

    def _initialize_default_provider(self) -> None:
        """Initialize default LLM provider based on settings."""
        if settings.LLM_PROVIDER == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not set in environment")
            
            self.llm_provider = OpenAIProvider(
                api_key=settings.OPENAI_API_KEY,
                model=settings.OPENAI_MODEL,
                base_url=settings.OPENAI_BASE_URL,
            )
            logger.info("OpenAI provider initialized as default")
        else:
            raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")

    def _get_default_system_prompt(self) -> str:
        """Get default system prompt."""
        return (
            f"You are {self.name}, a helpful, knowledgeable, and friendly AI assistant. "
            f"Your goal is to provide accurate, thoughtful, and helpful responses to user queries. "
            f"Always be honest about your limitations and uncertainties. "
            f"Provide clear explanations and examples when appropriate. "
            f"Be respectful and maintain a professional tone."
        )

    def chat(
        self,
        user_input: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """
        Process a user message and generate a response.

        Args:
            user_input: User's message
            temperature: Optional custom temperature
            max_tokens: Optional custom max tokens
            **kwargs: Additional parameters for the LLM

        Returns:
            Assistant's response string
        """
        # Validate input
        if not InputValidator.validate_string(user_input, min_length=1, max_length=10000):
            logger.warning("Invalid user input")
            return "I'm sorry, I couldn't process your input. Please try again."

        # Sanitize input
        user_input = InputValidator.sanitize_input(user_input)

        # Add to memory
        if self.memory:
            self.memory.add_user_message(user_input)
            logger.debug(f"User message added to memory. Total messages: {len(self.memory)}")

        try:
            # Prepare messages for LLM
            messages = self._prepare_messages()
            messages.append({"role": "user", "content": user_input})

            # Get response from LLM
            temperature = temperature or settings.TEMPERATURE
            max_tokens = max_tokens or settings.MAX_TOKENS

            logger.debug(f"Calling LLM with {len(messages)} messages")
            response = self.llm_provider.generate(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )

            # Extract and store response
            assistant_response = response.content

            if self.memory:
                self.memory.add_assistant_message(assistant_response)
                logger.debug(f"Assistant response added to memory")

            logger.info(f"Successfully generated response ({len(assistant_response)} chars)")
            return assistant_response

        except Exception as e:
            logger.error(f"Error in chat: {str(e)}")
            error_message = f"I encountered an error while processing your request: {str(e)}"
            
            if self.memory:
                self.memory.add_assistant_message(error_message)
            
            return error_message

    def _prepare_messages(self) -> List[Dict[str, str]]:
        """
        Prepare messages for LLM including system prompt and history.

        Returns:
            List of message dictionaries
        """
        messages = [{"role": "system", "content": self.system_prompt}]

        if self.memory and len(self.memory) > 0:
            # Get conversation history
            history = self.memory.get_messages()
            messages.extend(history)

        return messages

    def set_system_prompt(self, prompt: str) -> None:
        """
        Set a custom system prompt.

        Args:
            prompt: New system prompt
        """
        if not InputValidator.validate_string(prompt, min_length=10):
            logger.warning("System prompt too short")
            return
        
        self.system_prompt = prompt
        logger.info("System prompt updated")

    def clear_memory(self) -> None:
        """Clear conversation history."""
        if self.memory:
            self.memory.clear_memory()
            logger.info("Conversation memory cleared")

    def get_conversation_summary(self) -> str:
        """
        Get a summary of the conversation.

        Returns:
            Summary string
        """
        if not self.memory:
            return "Memory is disabled"
        
        return self.memory.get_summary()

    def export_conversation(self) -> List[Dict[str, Any]]:
        """
        Export full conversation history.

        Returns:
            List of message dictionaries
        """
        if not self.memory:
            return []
        
        return self.memory.export_history()

    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List available tools.

        Returns:
            List of tool information dictionaries
        """
        if not self.tools:
            return []
        
        return self.tools.list_tools()

    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Execute a tool.

        Args:
            tool_name: Name of the tool
            **kwargs: Tool arguments

        Returns:
            Tool execution result
        """
        if not self.tools:
            raise ValueError("Tools are not enabled")
        
        logger.debug(f"Executing tool: {tool_name}")
        return self.tools.execute_tool(tool_name, **kwargs)

    def set_context(self, key: str, value: Any) -> None:
        """
        Set a context variable.

        Args:
            key: Context variable name
            value: Context value
        """
        if self.memory:
            self.memory.set_context(key, value)
            logger.debug(f"Context set: {key}")

    def get_context(self) -> Dict[str, Any]:
        """
        Get current context.

        Returns:
            Context dictionary
        """
        if not self.memory:
            return {}
        
        return self.memory.get_context()

    def validate_provider(self) -> bool:
        """
        Validate LLM provider connection.

        Returns:
            True if provider is accessible
        """
        logger.info("Validating LLM provider connection...")
        is_valid = self.llm_provider.validate_connection()
        
        if is_valid:
            logger.info("LLM provider validation successful")
        else:
            logger.error("LLM provider validation failed")
        
        return is_valid

    def get_info(self) -> Dict[str, Any]:
        """
        Get assistant information.

        Returns:
            Dictionary with assistant info
        """
        return {
            'name': self.name,
            'llm_provider': self.llm_provider.__class__.__name__,
            'model': self.llm_provider.model,
            'memory_enabled': self.enable_memory,
            'tools_enabled': self.enable_tools,
            'memory_size': len(self.memory) if self.memory else 0,
            'tools_count': len(self.tools.tools) if self.tools else 0,
        }

    def __repr__(self) -> str:
        """String representation."""
        return f"PersonalAssistant(name={self.name}, provider={self.llm_provider.__class__.__name__})"
