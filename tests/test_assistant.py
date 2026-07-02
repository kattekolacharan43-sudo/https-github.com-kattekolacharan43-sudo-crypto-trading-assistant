"""
Unit tests for the PersonalAssistant class.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from core.assistant import PersonalAssistant
from integrations.llm_provider import LLMResponse


class TestPersonalAssistant(unittest.TestCase):
    """Test cases for PersonalAssistant."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a mock LLM provider
        self.mock_provider = Mock()
        self.mock_provider.generate.return_value = LLMResponse(
            content="Test response",
            model="test-model",
        )

    def test_assistant_initialization(self):
        """Test assistant initialization."""
        assistant = PersonalAssistant(
            name="TestAssistant",
            llm_provider=self.mock_provider,
        )

        self.assertEqual(assistant.name, "TestAssistant")
        self.assertIsNotNone(assistant.memory)
        self.assertIsNotNone(assistant.tools)

    def test_chat_with_valid_input(self):
        """Test chat with valid input."""
        assistant = PersonalAssistant(
            llm_provider=self.mock_provider,
        )

        response = assistant.chat("Hello, how are you?")

        self.assertEqual(response, "Test response")
        self.mock_provider.generate.assert_called_once()

    def test_chat_with_empty_input(self):
        """Test chat with empty input."""
        assistant = PersonalAssistant(
            llm_provider=self.mock_provider,
        )

        response = assistant.chat("   ")

        self.assertIn("couldn't process", response.lower())

    def test_memory_persistence(self):
        """Test that messages are stored in memory."""
        assistant = PersonalAssistant(
            llm_provider=self.mock_provider,
        )

        assistant.chat("First message")
        assistant.chat("Second message")

        self.assertEqual(len(assistant.memory), 4)  # 2 user + 2 assistant

    def test_clear_memory(self):
        """Test clearing conversation memory."""
        assistant = PersonalAssistant(
            llm_provider=self.mock_provider,
        )

        assistant.chat("Test message")
        self.assertGreater(len(assistant.memory), 0)

        assistant.clear_memory()
        self.assertEqual(len(assistant.memory), 0)

    def test_system_prompt_setting(self):
        """Test setting custom system prompt."""
        assistant = PersonalAssistant(
            llm_provider=self.mock_provider,
        )

        custom_prompt = "You are a test assistant for unit testing."
        assistant.set_system_prompt(custom_prompt)

        self.assertEqual(assistant.system_prompt, custom_prompt)

    def test_context_management(self):
        """Test context variable management."""
        assistant = PersonalAssistant(
            llm_provider=self.mock_provider,
        )

        assistant.set_context("user_id", "12345")
        assistant.set_context("language", "en")

        context = assistant.get_context()

        self.assertEqual(context["user_id"], "12345")
        self.assertEqual(context["language"], "en")

    def test_tool_listing(self):
        """Test listing available tools."""
        assistant = PersonalAssistant(
            llm_provider=self.mock_provider,
        )

        tools = assistant.list_tools()

        self.assertIsInstance(tools, list)
        self.assertGreater(len(tools), 0)

    def test_assistant_info(self):
        """Test getting assistant information."""
        assistant = PersonalAssistant(
            name="TestAssistant",
            llm_provider=self.mock_provider,
        )

        info = assistant.get_info()

        self.assertEqual(info["name"], "TestAssistant")
        self.assertTrue(info["memory_enabled"])
        self.assertTrue(info["tools_enabled"])
        self.assertGreater(info["tools_count"], 0)

    def test_conversation_export(self):
        """Test exporting conversation."""
        assistant = PersonalAssistant(
            llm_provider=self.mock_provider,
        )

        assistant.chat("Test message")

        history = assistant.export_conversation()

        self.assertIsInstance(history, list)
        self.assertGreater(len(history), 0)

    def test_memory_disabled(self):
        """Test assistant with memory disabled."""
        assistant = PersonalAssistant(
            llm_provider=self.mock_provider,
            enable_memory=False,
        )

        assistant.chat("Test message")

        self.assertIsNone(assistant.memory)
        self.assertEqual(len(assistant.export_conversation()), 0)

    def test_tools_disabled(self):
        """Test assistant with tools disabled."""
        assistant = PersonalAssistant(
            llm_provider=self.mock_provider,
            enable_tools=False,
        )

        self.assertIsNone(assistant.tools)
        self.assertEqual(len(assistant.list_tools()), 0)


class TestConversationFlow(unittest.TestCase):
    """Test cases for conversation flow."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_provider = Mock()
        self.mock_provider.generate.side_effect = [
            LLMResponse("I'm doing well, thanks for asking!", model="test"),
            LLMResponse("Python is a great programming language.", model="test"),
            LLMResponse("You're welcome! Have a great day.", model="test"),
        ]

    def test_multi_turn_conversation(self):
        """Test multi-turn conversation flow."""
        assistant = PersonalAssistant(
            llm_provider=self.mock_provider,
        )

        response1 = assistant.chat("How are you?")
        response2 = assistant.chat("Tell me about Python.")
        response3 = assistant.chat("Thanks for the info!")

        self.assertEqual(response1, "I'm doing well, thanks for asking!")
        self.assertEqual(response2, "Python is a great programming language.")
        self.assertEqual(response3, "You're welcome! Have a great day.")


if __name__ == "__main__":
    unittest.main()
