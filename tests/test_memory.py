"""
Unit tests for the ConversationMemory class.
"""

import unittest
from core.memory import ConversationMemory, Message


class TestConversationMemory(unittest.TestCase):
    """Test cases for ConversationMemory."""

    def setUp(self):
        """Set up test fixtures."""
        self.memory = ConversationMemory(max_messages=10)

    def test_memory_initialization(self):
        """Test memory initialization."""
        self.assertEqual(len(self.memory), 0)
        self.assertEqual(self.memory.max_messages, 10)

    def test_add_user_message(self):
        """Test adding user messages."""
        self.memory.add_user_message("Hello, assistant!")

        self.assertEqual(len(self.memory), 1)
        self.assertEqual(self.memory.messages[0].role, "user")
        self.assertEqual(self.memory.messages[0].content, "Hello, assistant!")

    def test_add_assistant_message(self):
        """Test adding assistant messages."""
        self.memory.add_assistant_message("Hello, user!")

        self.assertEqual(len(self.memory), 1)
        self.assertEqual(self.memory.messages[0].role, "assistant")

    def test_add_multiple_messages(self):
        """Test adding multiple messages."""
        self.memory.add_user_message("Hi")
        self.memory.add_assistant_message("Hello!")
        self.memory.add_user_message("How are you?")
        self.memory.add_assistant_message("I'm doing well!")

        self.assertEqual(len(self.memory), 4)

    def test_get_messages_format(self):
        """Test message format for LLM."""
        self.memory.add_user_message("Test")
        self.memory.add_assistant_message("Response")

        messages = self.memory.get_messages()

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[1]["role"], "assistant")
        self.assertIn("timestamp", messages[0])

    def test_get_last_n_messages(self):
        """Test getting last N messages."""
        for i in range(5):
            self.memory.add_user_message(f"Message {i}")

        last_3 = self.memory.get_last_n_messages(3)

        self.assertEqual(len(last_3), 3)
        self.assertEqual(last_3[0].content, "Message 2")
        self.assertEqual(last_3[2].content, "Message 4")

    def test_max_messages_limit(self):
        """Test max messages limit enforcement."""
        for i in range(15):
            self.memory.add_user_message(f"Message {i}")

        self.assertEqual(len(self.memory), 10)
        self.assertEqual(self.memory.messages[0].content, "Message 5")
        self.assertEqual(self.memory.messages[-1].content, "Message 14")

    def test_clear_memory(self):
        """Test clearing memory."""
        self.memory.add_user_message("Message 1")
        self.memory.add_user_message("Message 2")
        self.assertEqual(len(self.memory), 2)

        self.memory.clear_memory()

        self.assertEqual(len(self.memory), 0)

    def test_context_management(self):
        """Test context variable management."""
        self.memory.set_context("user_id", "123")
        self.memory.set_context("language", "en")

        context = self.memory.get_context()

        self.assertEqual(context["user_id"], "123")
        self.assertEqual(context["language"], "en")

    def test_update_context(self):
        """Test updating multiple context variables."""
        self.memory.update_context({
            "key1": "value1",
            "key2": "value2",
            "key3": "value3",
        })

        context = self.memory.get_context()

        self.assertEqual(len(context), 3)
        self.assertEqual(context["key1"], "value1")

    def test_add_message_with_metadata(self):
        """Test adding messages with metadata."""
        metadata = {"source": "web", "timestamp": "2024-01-01"}
        self.memory.add_user_message("Test", metadata=metadata)

        messages = self.memory.get_messages()

        self.assertEqual(messages[0]["metadata"]["source"], "web")

    def test_get_summary(self):
        """Test conversation summary."""
        self.memory.add_user_message("Hi")
        self.memory.add_assistant_message("Hello!")
        self.memory.add_user_message("How are you?")

        summary = self.memory.get_summary()

        self.assertIn("User messages: 2", summary)
        self.assertIn("Assistant messages: 1", summary)

    def test_export_history(self):
        """Test exporting conversation history."""
        self.memory.add_user_message("Message 1")
        self.memory.add_assistant_message("Response 1")

        history = self.memory.export_history()

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[1]["role"], "assistant")
        self.assertIn("timestamp", history[0])

    def test_empty_message_rejection(self):
        """Test that empty messages are rejected."""
        self.memory.add_user_message("")
        self.memory.add_user_message("   ")

        self.assertEqual(len(self.memory), 0)

    def test_get_messages_limit(self):
        """Test getting messages with limit."""
        for i in range(5):
            self.memory.add_user_message(f"Message {i}")

        # Get last 2 messages
        messages = self.memory.get_messages(limit=2)

        self.assertEqual(len(messages), 2)
        self.assertIn("Message 3", messages[0]["content"])
        self.assertIn("Message 4", messages[1]["content"])

    def test_message_to_dict(self):
        """Test converting message to dictionary."""
        self.memory.add_user_message("Test message")
        msg = self.memory.messages[0]

        msg_dict = msg.to_dict()

        self.assertEqual(msg_dict["role"], "user")
        self.assertEqual(msg_dict["content"], "Test message")
        self.assertIn("timestamp", msg_dict)

    def test_memory_repr(self):
        """Test memory string representation."""
        self.memory.add_user_message("Test")
        repr_str = repr(self.memory)

        self.assertIn("ConversationMemory", repr_str)
        self.assertIn("messages=1", repr_str)


if __name__ == "__main__":
    unittest.main()
