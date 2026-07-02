"""
Conversation memory management for the AI Assistant.
Maintains conversation history with context awareness.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Message:
    """Represents a single message in the conversation."""

    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata or {},
        }


class ConversationMemory:
    """Manages conversation history and context."""

    def __init__(self, max_messages: int = 50):
        """
        Initialize conversation memory.

        Args:
            max_messages: Maximum number of messages to retain
        """
        self.max_messages = max_messages
        self.messages: List[Message] = []
        self.context: Dict[str, Any] = {}
        logger.debug(f"ConversationMemory initialized with max_messages={max_messages}")

    def add_message(
        self,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Add a message to the conversation history.

        Args:
            role: 'user' or 'assistant'
            content: Message content
            metadata: Optional metadata about the message
        """
        if not content or not content.strip():
            logger.warning("Attempt to add empty message")
            return

        message = Message(
            role=role,
            content=content.strip(),
            timestamp=datetime.now(),
            metadata=metadata,
        )
        self.messages.append(message)
        logger.debug(f"Message added: {role} - {len(content)} chars")

        # Remove oldest message if limit exceeded
        if len(self.messages) > self.max_messages:
            removed = self.messages.pop(0)
            logger.debug(f"Removed oldest message to maintain limit")

    def add_user_message(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a user message."""
        self.add_message('user', content, metadata)

    def add_assistant_message(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add an assistant message."""
        self.add_message('assistant', content, metadata)

    def get_messages(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get message history in LLM-compatible format.

        Args:
            limit: Optional limit on number of messages to return

        Returns:
            List of message dictionaries
        """
        messages = self.messages
        if limit and limit > 0:
            messages = messages[-limit:]
        
        return [msg.to_dict() for msg in messages]

    def get_last_n_messages(self, n: int) -> List[Message]:
        """
        Get the last N messages.

        Args:
            n: Number of messages to return

        Returns:
            List of Message objects
        """
        return self.messages[-n:] if n > 0 else []

    def get_context(self) -> Dict[str, Any]:
        """Get conversation context."""
        return self.context.copy()

    def set_context(self, key: str, value: Any) -> None:
        """
        Set a context variable.

        Args:
            key: Context variable name
            value: Context value
        """
        self.context[key] = value
        logger.debug(f"Context set: {key}")

    def update_context(self, context_dict: Dict[str, Any]) -> None:
        """
        Update multiple context variables.

        Args:
            context_dict: Dictionary of context variables
        """
        self.context.update(context_dict)
        logger.debug(f"Context updated with {len(context_dict)} items")

    def clear_memory(self) -> None:
        """Clear all conversation history and context."""
        self.messages.clear()
        self.context.clear()
        logger.info("Conversation memory cleared")

    def get_summary(self) -> str:
        """
        Get a summary of the conversation.

        Returns:
            Summary string
        """
        if not self.messages:
            return "No conversation history"

        user_messages = len([m for m in self.messages if m.role == 'user'])
        assistant_messages = len([m for m in self.messages if m.role == 'assistant'])
        
        first_msg_time = self.messages[0].timestamp
        last_msg_time = self.messages[-1].timestamp
        duration = last_msg_time - first_msg_time

        return (
            f"Conversation Summary:\n"
            f"- User messages: {user_messages}\n"
            f"- Assistant messages: {assistant_messages}\n"
            f"- Duration: {duration}\n"
            f"- Total messages: {len(self.messages)}"
        )

    def export_history(self) -> List[Dict[str, Any]]:
        """
        Export complete conversation history.

        Returns:
            List of message dictionaries with full details
        """
        return [
            {
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat(),
                'metadata': msg.metadata or {},
            }
            for msg in self.messages
        ]

    def __len__(self) -> int:
        """Return number of messages in memory."""
        return len(self.messages)

    def __repr__(self) -> str:
        """String representation."""
        return f"ConversationMemory(messages={len(self.messages)}, context_keys={list(self.context.keys())})"
